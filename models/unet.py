"""
PyTorch 2D U-Net Architecture for Spatiotemporal Wildfire Spread Prediction.
Predicts Next-Day Wildfire Spread from 5 Environmental Channels:
- Channel 0: Fire Mask (t) - Current Ignition / Fire perimeter
- Channel 1: Elevation (DEM) - Normalized Terrain Altitude
- Channel 2: Vegetation Density (NDVI / Fuel moisture)
- Channel 3: Wind Vector U (East-West velocity component)
- Channel 4: Wind Vector V (North-South velocity component)

Output:
- Channel 0: Fire Spread Probability P(x, y) in [0.0, 1.0] at t+1
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Union
import numpy as np


class DoubleConv(nn.Module):
    """(Conv2D -> BatchNorm -> ReLU -> Dropout) * 2"""

    def __init__(self, in_channels: int, out_channels: int, dropout_p: float = 0.0):
        super().__init__()
        layers = [
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        ]
        if dropout_p > 0.0:
            layers.append(nn.Dropout2d(p=dropout_p))

        layers.extend([
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        ])
        if dropout_p > 0.0:
            layers.append(nn.Dropout2d(p=dropout_p))

        self.block = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class Down(nn.Module):
    """Downscaling with MaxPool2D then DoubleConv"""

    def __init__(self, in_channels: int, out_channels: int, dropout_p: float = 0.0):
        super().__init__()
        self.maxpool_conv = nn.Sequential(
            nn.MaxPool2d(2),
            DoubleConv(in_channels, out_channels, dropout_p=dropout_p),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.maxpool_conv(x)


class Up(nn.Module):
    """Upscaling via Bilinear Interpolation / ConvTranspose then DoubleConv with Skip Connection"""

    def __init__(self, in_channels: int, out_channels: int, bilinear: bool = True, dropout_p: float = 0.0):
        super().__init__()
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=True)
            self.conv = DoubleConv(in_channels, out_channels, dropout_p=dropout_p)
        else:
            self.up = nn.ConvTranspose2d(in_channels // 2, in_channels // 2, kernel_size=2, stride=2)
            self.conv = DoubleConv(in_channels, out_channels, dropout_p=dropout_p)

    def forward(self, x1: torch.Tensor, x2: torch.Tensor) -> torch.Tensor:
        x1 = self.up(x1)
        # Pad x1 if necessary to match x2's spatial dimensions
        diff_y = x2.size()[2] - x1.size()[2]
        diff_x = x2.size()[3] - x1.size()[3]
        if diff_y > 0 or diff_x > 0:
            x1 = F.pad(x1, [diff_x // 2, diff_x - diff_x // 2, diff_y // 2, diff_y - diff_y // 2])
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


class UNet2D(nn.Module):
    """
    Standard U-Net 2D for Wildfire Spread Prediction.
    in_channels=5: [Fire_t, Elevation, Vegetation, Wind_U, Wind_V]
    out_channels=1: Fire_t+1 (Sigmoid-activated spread probability)
    """

    def __init__(
        self,
        in_channels: int = 5,
        out_channels: int = 1,
        base_features: int = 32,
        bilinear: bool = True,
        dropout_p: float = 0.2,
    ):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.bilinear = bilinear

        # Encoder (Contracting Path)
        self.inc = DoubleConv(in_channels, base_features, dropout_p=0.0)
        self.down1 = Down(base_features, base_features * 2, dropout_p=dropout_p * 0.5)
        self.down2 = Down(base_features * 2, base_features * 4, dropout_p=dropout_p)
        self.down3 = Down(base_features * 4, base_features * 8, dropout_p=dropout_p * 1.5)

        # Decoder (Expansive Path with Skip Connections)
        # up1: 256 (from down3) + 128 (skip from down2) -> 128
        self.up1 = Up(base_features * 8 + base_features * 4, base_features * 4, bilinear, dropout_p=dropout_p)
        # up2: 128 (from up1) + 64 (skip from down1) -> 64
        self.up2 = Up(base_features * 4 + base_features * 2, base_features * 2, bilinear, dropout_p=dropout_p * 0.5)
        # up3: 64 (from up2) + 32 (skip from inc) -> 32
        self.up3 = Up(base_features * 2 + base_features, base_features, bilinear, dropout_p=0.0)

        # Final 1x1 Convolution
        self.outc = nn.Conv2d(base_features, out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor, return_logits: bool = False) -> torch.Tensor:
        # Encoder
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)

        # Decoder + Skip Connections
        x = self.up1(x4, x3)
        x = self.up2(x, x2)
        x = self.up3(x, x1)

        logits = self.outc(x)
        if return_logits:
            return logits
        return torch.sigmoid(logits)


# Alias for backward compatibility
FireUNet = UNet2D


def predict_fire_heatmap(
    model: nn.Module,
    current_grid_tensor: Union[torch.Tensor, np.ndarray],
    device: str = "cpu",
    threshold: float = 0.5,
) -> np.ndarray:
    """
    Inference helper:
    Receives 2D multi-channel tensor/array (5, H, W) or (1, 5, H, W),
    runs forward pass on the U-Net model, and returns a 2D float NumPy matrix
    containing fire spread probability P(x, y) in [0.0, 1.0] for the A* pathfinding module.
    """
    model.eval()
    dev = torch.device(device)
    model.to(dev)

    if isinstance(current_grid_tensor, np.ndarray):
        arr = current_grid_tensor.astype(np.float32)
        if arr.ndim == 3:  # (5, H, W)
            tensor = torch.from_numpy(arr).unsqueeze(0)  # (1, 5, H, W)
        elif arr.ndim == 4:  # (B, 5, H, W)
            tensor = torch.from_numpy(arr)
        else:
            raise ValueError(f"Expected 3D or 4D array, got shape {arr.shape}")
    elif isinstance(current_grid_tensor, torch.Tensor):
        tensor = current_grid_tensor.float()
        if tensor.ndim == 3:
            tensor = tensor.unsqueeze(0)
    else:
        raise TypeError(f"Unsupported input type {type(current_grid_tensor)}")

    tensor = tensor.to(dev)

    with torch.no_grad():
        pred_prob = model(tensor, return_logits=False)  # (1, 1, H, W)
        heatmap = pred_prob.squeeze().cpu().numpy()  # (H, W)

    # Ensure float32 in [0.0, 1.0]
    return np.clip(heatmap.astype(np.float32), 0.0, 1.0)
