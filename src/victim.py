"""
Victim model for Wildfire Rescue Swarm.
Defines Victim state, health urgency, priority levels, and rescue transitions.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, Dict, Any


class VictimStatus(str, Enum):
    WAITING = "waiting"
    RESCUED = "rescued"
    TRAPPED = "trapped"
    DEAD = "dead"


@dataclass
class Victim:
    id: int
    position: Tuple[int, int]  # (x, y)
    priority: int = 1  # 1: Low, 2: Medium, 3: High
    max_wait_time: int = 60  # Maximum time steps before conditions become critical
    rescue_duration: int = 2  # Time required by a robot at site to complete rescue
    status: VictimStatus = VictimStatus.WAITING
    remaining_wait_time: int = field(init=False)
    time_spent_rescuing: int = 0

    def __post_init__(self):
        self.remaining_wait_time = self.max_wait_time

    @property
    def x(self) -> int:
        return self.position[0]

    @property
    def y(self) -> int:
        return self.position[1]

    @property
    def is_active(self) -> bool:
        return self.status in (VictimStatus.WAITING, VictimStatus.TRAPPED)

    def step_decay(self, in_fire: bool = False):
        """Decrements wait time. If inside fire, health decays 3x faster."""
        if not self.is_active:
            return

        if in_fire:
            self.remaining_wait_time = max(0, self.remaining_wait_time - 3)
            if self.remaining_wait_time <= 0:
                self.status = VictimStatus.DEAD
        else:
            self.remaining_wait_time = max(0, self.remaining_wait_time - 1)
            if self.remaining_wait_time <= 0:
                self.status = VictimStatus.TRAPPED

    def mark_rescued(self):
        self.status = VictimStatus.RESCUED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "position": list(self.position),
            "priority": self.priority,
            "max_wait_time": self.max_wait_time,
            "remaining_wait_time": self.remaining_wait_time,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Victim":
        pos = tuple(data["position"]) if "position" in data else (data["x"], data["y"])
        v = cls(
            id=data["id"],
            position=pos,
            priority=data.get("priority", 1),
            max_wait_time=data.get("max_wait_time", 60),
            rescue_duration=data.get("rescue_duration", 2),
        )
        if "status" in data:
            v.status = VictimStatus(data["status"])
        if "remaining_wait_time" in data:
            v.remaining_wait_time = data["remaining_wait_time"]
        return v
