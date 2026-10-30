"""
Production Deep Learning Training Script for Wildfire Spread Prediction.
Dataset: Next Day Wildfire Spread (Kaggle / Google Research: fantineh/next-day-wildfire-spread).
Framework: PyTorch 2D U-Net (5 input channels -> 1 probability channel).

Features:
1. 70% Train / 30% Test reproducible split with fixed seed=42.
2. UNet2D(in_channels=5, out_channels=1) with Skip Connections & Dropout.
3. BCEDiceLoss for handling severe class imbalance.
4. Comprehensive metrics: Val Loss, Precision, Recall, F1-Score, IoU.
5. Anti-Overfitting: Spatial Data Augmentation (Flip, Rotate), AdamW weight decay, CosineAnnealingLR.
6. Auto-saves best model by highest F1-Score to models/best_unet_fire.pth.
7. Exports logs/training_metrics.csv and plots logs/loss_curve.png.
8. predict_fire_heatmap() for seamless integration with A* and simulation engine.
"""

import os
import sys
import glob
import json
import random
from typing import Tuple, Dict, Any, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# Ensure models module can be imported
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)
sys.path.insert(0, PROJECT_DIR)

from unet import UNet2D, predict_fire_heatmap


# ==============================================================================
# 1. REPRODUCIBILITY SEEDING
# ==============================================================================
def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


set_seed(42)


# ==============================================================================
# 2. DATA AUGMENTATION (ANTI-OVERFITTING)
# ==============================================================================
class SpatialAugmenter:
    """
    On-the-fly geometric data augmentation to prevent overfitting:
    - Random Horizontal Flip (p=0.5)
    - Random Vertical Flip (p=0.5)
    - Random 90, 180, 270 degree rotation (p=0.5)
    - Wind vector coordinate transformation under geometric rotation
    """

    def __init__(self, p_flip: float = 0.5, p_rot: float = 0.5):
        self.p_flip = p_flip
        self.p_rot = p_rot

    def __call__(self, x: torch.Tensor, y: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # x: (5, H, W) -> [Fire_t, Elevation, Vegetation, Wind_U, Wind_V]
        # y: (1, H, W) -> [Fire_t+1]

        # Horizontal Flip
        if random.random() < self.p_flip:
            x = torch.flip(x, dims=[-1])
            y = torch.flip(y, dims=[-1])
            x[3] = -x[3]  # Flip Wind U component

        # Vertical Flip
        if random.random() < self.p_flip:
            x = torch.flip(x, dims=[-2])
            y = torch.flip(y, dims=[-2])
            x[4] = -x[4]  # Flip Wind V component

        # 90-degree Rotations
        if random.random() < self.p_rot:
            k = random.choice([1, 2, 3])
            x = torch.rot90(x, k=k, dims=[-2, -1])
            y = torch.rot90(y, k=k, dims=[-2, -1])
            # Adjust wind vectors under rotation
            u, v = x[3].clone(), x[4].clone()
            if k == 1:    # 90 deg counter-clockwise
                x[3], x[4] = -v, u
            elif k == 2:  # 180 deg
                x[3], x[4] = -u, -v
            elif k == 3:  # 270 deg
                x[3], x[4] = v, -u

        return x, y


# ==============================================================================
# 3. DATASET LOADER (KAGGLE "NEXT DAY WILDFIRE SPREAD" / SYNTHETIC FALLBACK)
# ==============================================================================
class WildfireDataset(Dataset):
    def __init__(self, data_x: np.ndarray, data_y: np.ndarray, transform=None):
        self.x = torch.tensor(data_x, dtype=torch.float32)
        self.y = torch.tensor(data_y, dtype=torch.float32)
        self.transform = transform

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        x = self.x[idx]
        y = self.y[idx]
        if self.transform:
            x, y = self.transform(x, y)
        return x, y


def generate_next_day_wildfire_samples(num_samples: int = 600, grid_size: int = 32, seed: int = 42):
    """
    Synthesizes samples matching the Google Research Next Day Wildfire Spread schema:
    Channels:
      0: Fire mask t (binary)
      1: Elevation DEM (normalized smooth gradient)
      2: Vegetation / Fuel density NDVI [0.1, 1.0]
      3: Wind U (East-West velocity component)
      4: Wind V (North-South velocity component)
    Target:
      Fire mask t+1 (binary propagation ground-truth)
    """
    rng = np.random.RandomState(seed)
    all_x = []
    all_y = []

    for _ in range(num_samples):
        # 0. Fire t (initial cluster)
        fire_t = np.zeros((grid_size, grid_size), dtype=np.float32)
        num_ignitions = rng.randint(1, 4)
        for _ in range(num_ignitions):
            cx, cy = rng.randint(4, grid_size - 4), rng.randint(4, grid_size - 4)
            fire_t[cy, cx] = 1.0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= cy + dy < grid_size and 0 <= cx + dx < grid_size and rng.rand() < 0.4:
                        fire_t[cy + dy, cx + dx] = 1.0

        # 1. Elevation DEM (sloped surface with hilltops)
        x_coord, y_coord = np.meshgrid(np.linspace(0, 1, grid_size), np.linspace(0, 1, grid_size))
        elev_slope = rng.uniform(-1, 1) * x_coord + rng.uniform(-1, 1) * y_coord
        elev_noise = rng.normal(0, 0.1, size=(grid_size, grid_size))
        elevation = (elev_slope + elev_noise - elev_slope.min()) / (elev_slope.max() - elev_slope.min() + 1e-5)

        # 2. Vegetation NDVI
        vegetation = rng.uniform(0.3, 1.0, size=(grid_size, grid_size)).astype(np.float32)

        # 3 & 4. Wind field (U, V)
        wind_angle = rng.uniform(0, 2 * np.pi)
        wind_speed = rng.uniform(0.5, 3.0)
        wind_u = np.full((grid_size, grid_size), np.cos(wind_angle) * wind_speed, dtype=np.float32)
        wind_v = np.full((grid_size, grid_size), np.sin(wind_angle) * wind_speed, dtype=np.float32)

        # Ground truth propagation for t+1 (Physics Cellular Automata)
        fire_t1 = np.copy(fire_t)
        burning = np.argwhere(fire_t == 1.0)
        for by, bx in burning:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = by + dy, bx + dx
                    if 0 <= ny < grid_size and 0 <= nx < grid_size:
                        if fire_t[ny, nx] == 0.0:
                            dist = np.hypot(dx, dy)
                            wind_dot = (dx * wind_u[by, bx] + dy * wind_v[by, bx]) / (dist * wind_speed + 1e-5)
                            slope_effect = (elevation[ny, nx] - elevation[by, bx]) * 2.0  # Fire climbs uphill faster
                            prob = 0.28 * vegetation[ny, nx] * max(0.2, 1.0 + 0.5 * wind_dot + slope_effect)
                            if rng.rand() < prob:
                                fire_t1[ny, nx] = 1.0

        sample_x = np.stack([fire_t, elevation.astype(np.float32), vegetation, wind_u, wind_v], axis=0)
        sample_y = np.expand_dims(fire_t1, axis=0)

        all_x.append(sample_x)
        all_y.append(sample_y)

    return np.array(all_x, dtype=np.float32), np.array(all_y, dtype=np.float32)


def load_dataset(data_dir: str = None, seed: int = 42) -> Tuple[WildfireDataset, WildfireDataset]:
    """
    Loads Next Day Wildfire Spread dataset.
    Splits into 70% Train Set and 30% Test Set / Environment Scenarios.
    """
    if data_dir is None:
        data_dir = os.path.join(PROJECT_DIR, "data", "wildfire_raw")

    # Check for raw Kaggle dataset (.npz or .npy files)
    raw_files = glob.glob(os.path.join(data_dir, "*.npz"))
    if raw_files:
        print(f"Loading raw Kaggle Next Day Wildfire Spread dataset from {raw_files[0]}...")
        data = np.load(raw_files[0])
        x_all = data["x"]  # (N, 5, H, W)
        y_all = data["y"]  # (N, 1, H, W)
    else:
        print("Raw Kaggle dataset not found locally. Synthesizing Google Research Next Day Wildfire schema dataset...")
        x_all, y_all = generate_next_day_wildfire_samples(num_samples=600, grid_size=32, seed=seed)

    # 70% Train / 30% Test Split
    n_total = len(x_all)
    indices = np.arange(n_total)
    rng = np.random.RandomState(seed)
    rng.shuffle(indices)

    split_idx = int(n_total * 0.70)
    train_idx = indices[:split_idx]
    test_idx = indices[split_idx:]

    print(f"Dataset Partitioning: Total={n_total} | Train (70%)={len(train_idx)} | Test (30%)={len(test_idx)}")

    train_dataset = WildfireDataset(x_all[train_idx], y_all[train_idx], transform=SpatialAugmenter())
    test_dataset = WildfireDataset(x_all[test_idx], y_all[test_idx], transform=None)

    return train_dataset, test_dataset


# ==============================================================================
# 4. LOSS FUNCTION: BCEDiceLoss (IMBALANCED FIRE DATA)
# ==============================================================================
class BCEDiceLoss(nn.Module):
    """
    Hybrid BCE + Soft Dice Loss for imbalanced segmentation.
    BCE stabilizes gradient descent, Dice focuses on the minority foreground (fire pixels).
    """

    def __init__(self, bce_weight: float = 0.5, dice_weight: float = 0.5, smooth: float = 1e-6):
        super().__init__()
        self.bce_weight = bce_weight
        self.dice_weight = dice_weight
        self.smooth = smooth
        self.bce_loss = nn.BCEWithLogitsLoss()

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        # BCE with raw logits for numerical stability
        bce = self.bce_loss(logits, targets)

        # Soft Dice on sigmoid probabilities
        probs = torch.sigmoid(logits)
        probs_flat = probs.view(-1)
        targets_flat = targets.view(-1)

        intersection = (probs_flat * targets_flat).sum()
        dice = 1.0 - ((2.0 * intersection + self.smooth) / (probs_flat.sum() + targets_flat.sum() + self.smooth))

        return (self.bce_weight * bce) + (self.dice_weight * dice)


# ==============================================================================
# 5. METRIC COMPUTATION (PRECISION, RECALL, F1-SCORE, IOU)
# ==============================================================================
def compute_metrics(preds_prob: torch.Tensor, targets: torch.Tensor, threshold: float = 0.5) -> Dict[str, float]:
    """Computes Precision, Recall, F1-Score, and IoU on binary masks."""
    preds_binary = (preds_prob >= threshold).float()
    targets = targets.float()

    tp = (preds_binary * targets).sum().item()
    fp = (preds_binary * (1.0 - targets)).sum().item()
    fn = ((1.0 - preds_binary) * targets).sum().item()

    smooth = 1e-6
    precision = tp / (tp + fp + smooth)
    recall = tp / (tp + fn + smooth)
    f1 = 2 * (precision * recall) / (precision + recall + smooth)
    iou = tp / (tp + fp + fn + smooth)

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "iou": iou,
    }


# ==============================================================================
# 6. TRAINING & EVALUATION PIPELINE
# ==============================================================================
def train_model(
    epochs: int = 20,
    batch_size: int = 16,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
    device: str = "cpu",
    seed: int = 42,
):
    set_seed(seed)
    dev = torch.device(device)

    print("=" * 80)
    print("🔥 WILDFIRE U-NET 2D TRAINING (NEXT DAY WILDFIRE SPREAD)")
    print("=" * 80)
    print(f"Device: {dev} | Seed: {seed} | Epochs: {epochs} | Batch Size: {batch_size}")

    train_ds, test_ds = load_dataset(seed=seed)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    model = UNet2D(in_channels=5, out_channels=1, base_features=32, dropout_p=0.2)
    model.to(dev)

    criterion = BCEDiceLoss(bce_weight=0.5, dice_weight=0.5)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    logs_dir = os.path.join(PROJECT_DIR, "logs")
    models_dir = os.path.join(PROJECT_DIR, "models")
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    best_f1 = -1.0
    best_epoch = 0
    best_weights_path = os.path.join(models_dir, "best_unet_fire.pth")
    metrics_log = []

    print("-" * 80)
    print(f"{'Epoch':<6} | {'Train Loss':<11} | {'Val Loss':<10} | {'Precision':<10} | {'Recall':<8} | {'F1-Score':<9} | {'IoU':<8} | {'Status'}")
    print("-" * 80)

    for epoch in range(1, epochs + 1):
        # Training Phase
        model.train()
        train_loss = 0.0
        for bx, by in train_loader:
            bx, by = bx.to(dev), by.to(dev)
            optimizer.zero_grad()
            logits = model(bx, return_logits=True)
            loss = criterion(logits, by)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
            optimizer.step()
            train_loss += loss.item() * len(bx)
        train_loss /= len(train_ds)

        # Evaluation Phase on 30% Test Set
        model.eval()
        val_loss = 0.0
        all_preds = []
        all_targets = []
        with torch.no_grad():
            for vx, vy in test_loader:
                vx, vy = vx.to(dev), vy.to(dev)
                v_logits = model(vx, return_logits=True)
                loss = criterion(v_logits, vy)
                val_loss += loss.item() * len(vx)
                all_preds.append(torch.sigmoid(v_logits).cpu())
                all_targets.append(vy.cpu())

        val_loss /= len(test_ds)
        cat_preds = torch.cat(all_preds, dim=0)
        cat_targets = torch.cat(all_targets, dim=0)
        eval_metrics = compute_metrics(cat_preds, cat_targets, threshold=0.5)

        scheduler.step()
        curr_lr = optimizer.param_groups[0]["lr"]

        is_best = eval_metrics["f1_score"] > best_f1
        status = "⭐ Best" if is_best else ""

        if is_best:
            best_f1 = eval_metrics["f1_score"]
            best_epoch = epoch
            torch.save(model.state_dict(), best_weights_path)
            # Also sync to wildfire_unet.pth for the existing engine
            torch.save(model.state_dict(), os.path.join(models_dir, "wildfire_unet.pth"))

        metrics_record = {
            "epoch": epoch,
            "train_loss": round(train_loss, 4),
            "val_loss": round(val_loss, 4),
            "precision": round(eval_metrics["precision"], 4),
            "recall": round(eval_metrics["recall"], 4),
            "f1_score": round(eval_metrics["f1_score"], 4),
            "iou": round(eval_metrics["iou"], 4),
            "learning_rate": curr_lr,
        }
        metrics_log.append(metrics_record)

        print(
            f"{epoch:02d}/{epochs:02d} | "
            f"{train_loss:10.4f} | "
            f"{val_loss:9.4f} | "
            f"{eval_metrics['precision']:9.4f} | "
            f"{eval_metrics['recall']:7.4f} | "
            f"{eval_metrics['f1_score']:8.4f} | "
            f"{eval_metrics['iou']:7.4f} | "
            f"{status}"
        )

    print("-" * 80)
    print(f"✅ Training Finished! Best F1-Score: {best_f1:.4f} at Epoch {best_epoch}.")
    print(f"💾 Best weights saved to: {best_weights_path}")

    # Export metrics CSV
    csv_path = os.path.join(logs_dir, "training_metrics.csv")
    df_metrics = pd.DataFrame(metrics_log)
    df_metrics.to_csv(csv_path, index=False)
    print(f"📊 Training log exported to: {csv_path}")

    # Plot Loss & F1 Curves
    plot_path = os.path.join(logs_dir, "loss_curve.png")
    plot_training_curves(df_metrics, plot_path)
    print(f"📈 Loss and Metrics curves saved to: {plot_path}")

    # Save JSON summary for dashboard
    summary_path = os.path.join(models_dir, "training_history.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "epochs": df_metrics["epoch"].tolist(),
            "train_loss": df_metrics["train_loss"].tolist(),
            "val_loss": df_metrics["val_loss"].tolist(),
            "f1_score": df_metrics["f1_score"].tolist(),
            "iou": df_metrics["iou"].tolist(),
            "precision": df_metrics["precision"].tolist(),
            "recall": df_metrics["recall"].tolist(),
            "best_f1": best_f1,
            "best_epoch": best_epoch,
        }, f, indent=2)

    return model, df_metrics


def plot_training_curves(df: pd.DataFrame, save_path: str):
    """Plots training and validation loss, F1-Score, and IoU curves."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Loss Curves
    ax1.plot(df["epoch"], df["train_loss"], "o-", color="#e53e3e", label="Train Loss (BCEDice)", linewidth=2)
    ax1.plot(df["epoch"], df["val_loss"], "s--", color="#3182ce", label="Val Loss (30% Test)", linewidth=2)
    ax1.set_title("U-Net Loss Convergence", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="upper right")

    # Evaluation Metrics Curves
    ax2.plot(df["epoch"], df["f1_score"], "o-", color="#38a169", label="F1-Score", linewidth=2)
    ax2.plot(df["epoch"], df["iou"], "^-", color="#805ad5", label="IoU", linewidth=2)
    ax2.plot(df["epoch"], df["precision"], ":", color="#dd6b20", label="Precision", linewidth=1.5)
    ax2.plot(df["epoch"], df["recall"], ":", color="#319795", label="Recall", linewidth=1.5)
    ax2.set_title("Segmentation Performance Metrics (30% Test Set)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Score [0.0 - 1.0]")
    ax2.set_ylim([0.0, 1.05])
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="lower right")

    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    device_name = "cuda" if torch.cuda.is_available() else "cpu"
    train_model(epochs=18, batch_size=16, lr=1e-3, device=device_name, seed=42)
