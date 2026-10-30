"""
Fire Simulation and U-Net-based Risk Prediction Module.
Implements Cellular Automata fire propagation and Deep Learning spatiotemporal risk estimation.
"""

import os
from typing import List, Tuple, Optional, Set
import numpy as np
import torch

from models.unet import UNet2D, predict_fire_heatmap


class FirePredictor:
    """Wrapper for U-Net 2D wildfire spread probability prediction."""

    def __init__(self, model_path: Optional[str] = None, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = UNet2D(in_channels=5, out_channels=1, base_features=32)

        if model_path is None:
            # Check for best_unet_fire.pth first, then wildfire_unet.pth
            curr = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            best_path = os.path.join(curr, "models", "best_unet_fire.pth")
            fallback_path = os.path.join(curr, "models", "wildfire_unet.pth")
            model_path = best_path if os.path.exists(best_path) else fallback_path

        if os.path.exists(model_path):
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.to(self.device)
            self.model.eval()
            self.is_loaded = True
        else:
            self.is_loaded = False

    def predict_risk_map(
        self,
        fire_grid: np.ndarray,
        fuel_grid: np.ndarray,
        wind_direction: Tuple[float, float] = (1.0, 0.0),
        wind_speed: float = 1.0,
        elevation_grid: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """
        Predicts continuous fire ignition risk probability for each cell [0.0, 1.0]
        using the 5-channel Next Day Wildfire Spread schema.
        """
        rows, cols = fire_grid.shape
        wind_u = np.full((rows, cols), wind_direction[0] * wind_speed, dtype=np.float32)
        wind_v = np.full((rows, cols), wind_direction[1] * wind_speed, dtype=np.float32)

        if elevation_grid is None:
            elevation_grid = np.zeros((rows, cols), dtype=np.float32)

        if not self.is_loaded:
            return self._heuristic_risk(fire_grid, fuel_grid, (wind_direction[0], wind_direction[1]), wind_speed)

        # 5 Channels: [Fire_t, Elevation, Vegetation/Fuel, Wind_U, Wind_V]
        inp = np.stack([
            (fire_grid == 1).astype(np.float32),
            elevation_grid.astype(np.float32),
            fuel_grid.astype(np.float32),
            wind_u,
            wind_v,
        ], axis=0)

        risk = predict_fire_heatmap(self.model, inp, device=str(self.device))

        # Active burning cells remain impassable (1.0)
        risk = np.clip(np.maximum(risk, (fire_grid == 1).astype(np.float32)), 0.0, 1.0)
        return risk

    def _heuristic_risk(
        self,
        fire_grid: np.ndarray,
        fuel_grid: np.ndarray,
        wind_dir: Tuple[float, float],
        wind_speed: float
    ) -> np.ndarray:
        rows, cols = fire_grid.shape
        risk = np.copy(fire_grid).astype(np.float32)
        fires = np.argwhere(fire_grid > 0)
        for fy, fx in fires:
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    ny, nx = fy + dy, fx + dx
                    if 0 <= ny < rows and 0 <= nx < cols:
                        dist = np.hypot(dx, dy)
                        if dist > 0:
                            wind_dot = (dx * wind_dir[0] + dy * wind_dir[1]) / (dist + 1e-5)
                            factor = max(0.0, 1.0 + 0.4 * wind_dot * wind_speed)
                            r = (1.0 / (1.0 + dist)) * factor * fuel_grid[ny, nx] * 0.5
                            risk[ny, nx] = max(risk[ny, nx], r)
        return np.clip(risk, 0.0, 1.0)


class FireSimulator:
    """Cellular Automaton wildfire spread model."""

    def __init__(
        self,
        rows: int = 20,
        cols: int = 20,
        initial_fires: Optional[List[Tuple[int, int]]] = None,
        obstacles: Optional[List[Tuple[int, int]]] = None,
        base_spread_prob: float = 0.25,
        wind_direction: Tuple[float, float] = (1.0, 0.0),
        wind_speed: float = 1.0,
        seed: int = 42,
    ):
        self.rows = rows
        self.cols = cols
        self.base_spread_prob = base_spread_prob
        self.wind_direction = wind_direction
        self.wind_speed = wind_speed
        self.rng = np.random.RandomState(seed)

        self.fire_grid = np.zeros((rows, cols), dtype=np.uint8)
        self.burn_duration_grid = np.zeros((rows, cols), dtype=np.int32)
        self.fuel_grid = np.ones((rows, cols), dtype=np.float32)
        self.obstacle_set: Set[Tuple[int, int]] = set(obstacles or [])

        # Non-burnable obstacles
        for ox, oy in self.obstacle_set:
            if 0 <= oy < rows and 0 <= ox < cols:
                self.fuel_grid[oy, ox] = 0.0

        if initial_fires:
            for fx, fy in initial_fires:
                if 0 <= fy < rows and 0 <= fx < cols and (fx, fy) not in self.obstacle_set:
                    self.fire_grid[fy, fx] = 1
                    self.burn_duration_grid[fy, fx] = 1

    def step(self) -> List[Tuple[int, int]]:
        """Advances fire by 1 step, returns newly ignited cells (x, y)."""
        new_fire = np.copy(self.fire_grid)
        burning = np.argwhere(self.fire_grid == 1)
        newly_ignited = []

        for fy, fx in burning:
            self.burn_duration_grid[fy, fx] += 1
            # After burning for 20 steps, fuel is exhausted -> burnt out (state 2)
            if self.burn_duration_grid[fy, fx] > 20:
                new_fire[fy, fx] = 2
                self.fuel_grid[fy, fx] = 0.0
                continue

            # 8-connected neighborhood
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = fy + dy, fx + dx
                    if 0 <= ny < self.rows and 0 <= nx < self.cols:
                        if self.fire_grid[ny, nx] == 0 and (nx, ny) not in self.obstacle_set:
                            dist = np.hypot(dx, dy)
                            dot = (dx * self.wind_direction[0] + dy * self.wind_direction[1]) / (dist + 1e-5)
                            wind_multiplier = max(0.3, 1.0 + 0.4 * dot * self.wind_speed)
                            fuel = self.fuel_grid[ny, nx]
                            p = (self.base_spread_prob * 0.35) * (1.0 / dist) * fuel * wind_multiplier

                            if self.rng.rand() < p:
                                new_fire[ny, nx] = 1
                                self.burn_duration_grid[ny, nx] = 1
                                newly_ignited.append((nx, ny))

        self.fire_grid = new_fire
        return newly_ignited

    def get_burning_cells(self) -> List[Tuple[int, int]]:
        coords = np.argwhere(self.fire_grid == 1)
        return [(int(c[1]), int(c[0])) for c in coords]  # (x, y)

    def is_burning(self, x: int, y: int) -> bool:
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return bool(self.fire_grid[y, x] == 1)
        return False
