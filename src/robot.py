"""
Robot Model and Dynamic Replanning Logic for Swarm Wildfire Rescue.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple, Optional, Set, Dict, Any
import numpy as np

from .astar import standard_astar, fire_aware_astar


class RobotStatus(str, Enum):
    IDLE = "idle"
    MOVING = "moving"
    RESCUING = "rescuing"
    BLOCKED = "blocked"
    COMPLETED = "completed"


@dataclass
class Robot:
    id: int
    position: Tuple[int, int]  # (x, y)
    status: RobotStatus = RobotStatus.IDLE
    current_target_id: Optional[int] = None
    target_queue: List[int] = field(default_factory=list)
    path: List[Tuple[int, int]] = field(default_factory=list)

    # Performance metrics
    total_distance: int = 0
    replanning_count: int = 0
    fire_risk_exposure: int = 0
    rescuing_timer: int = 0

    @property
    def x(self) -> int:
        return self.position[0]

    @property
    def y(self) -> int:
        return self.position[1]

    def set_target(self, victim_id: int):
        self.current_target_id = victim_id
        self.rescuing_timer = 0

    def set_queue(self, queue: List[int]):
        self.target_queue = list(queue)
        if self.current_target_id is None and self.target_queue:
            self.current_target_id = self.target_queue.pop(0)
            self.rescuing_timer = 0

    def pop_next_target(self) -> Optional[int]:
        while self.target_queue:
            next_id = self.target_queue.pop(0)
            self.current_target_id = next_id
            self.rescuing_timer = 0
            return next_id
        self.current_target_id = None
        self.status = RobotStatus.IDLE
        return None

    def should_replan(
        self,
        fires: Set[Tuple[int, int]],
        risk_map: Optional[np.ndarray] = None,
        risk_threshold: float = 0.65,
    ) -> bool:
        """
        Determines if the current trajectory is compromised by advancing fire.
        Replanning is triggered if:
        1. Any remaining waypoint on path is on fire.
        2. In proposed mode, if upcoming waypoints enter high fire-risk zones.
        """
        if not self.path:
            return False

        # Lookahead along remaining path
        for pt in self.path[:5]:
            if pt in fires:
                return True
            if risk_map is not None:
                px, py = pt
                if 0 <= py < risk_map.shape[0] and 0 <= px < risk_map.shape[1]:
                    if risk_map[py, px] >= risk_threshold:
                        return True
        return False

    def plan_path(
        self,
        goal: Tuple[int, int],
        grid_shape: Tuple[int, int],
        obstacles: Set[Tuple[int, int]],
        fires: Set[Tuple[int, int]],
        mode: str = "proposed",
        risk_map: Optional[np.ndarray] = None,
        risk_weight: float = 8.0,
        safety_buffer_radius: int = 2,
    ) -> bool:
        """Plans or replans trajectory towards goal."""
        if mode == "baseline":
            new_path = standard_astar(
                start=self.position,
                goal=goal,
                grid_shape=grid_shape,
                obstacles=obstacles,
                fires=fires,
            )
        else:
            if risk_map is None:
                risk_map = np.zeros(grid_shape, dtype=np.float32)
            new_path = fire_aware_astar(
                start=self.position,
                goal=goal,
                grid_shape=grid_shape,
                obstacles=obstacles,
                fires=fires,
                risk_map=risk_map,
                risk_weight=risk_weight,
                safety_buffer_radius=safety_buffer_radius,
            )

        if new_path is not None and len(new_path) > 1:
            # Exclude current position from path queue
            self.path = new_path[1:]
            self.status = RobotStatus.MOVING
            return True
        elif new_path is not None and len(new_path) == 1:
            self.path = []
            return True
        else:
            self.path = []
            self.status = RobotStatus.BLOCKED
            return False

    def step_move(
        self,
        fires: Set[Tuple[int, int]],
        risk_map: Optional[np.ndarray] = None,
    ) -> Tuple[int, int]:
        """Executes one step along the path."""
        if self.path and self.status == RobotStatus.MOVING:
            next_step = self.path.pop(0)

            # Check fire hazard exposure (Ground-truth physical metric)
            if next_step in fires:
                self.fire_risk_exposure += 3
            else:
                is_near_fire = any(abs(next_step[0] - fx) + abs(next_step[1] - fy) <= 1 for fx, fy in fires)
                if is_near_fire:
                    self.fire_risk_exposure += 1

            self.position = next_step
            self.total_distance += 1

            if not self.path:
                self.status = RobotStatus.IDLE

        return self.position

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "position": list(self.position),
            "status": self.status.value,
            "target_victim_id": self.current_target_id,
            "path": [{"x": p[0], "y": p[1]} for p in self.path],
            "total_distance": self.total_distance,
            "replanning_count": self.replanning_count,
            "fire_risk_exposure": self.fire_risk_exposure,
        }
