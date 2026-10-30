"""
Wildfire Rescue Swarm Intelligence Framework
A modular, reproducible benchmark for multi-agent robotic search and rescue in dynamic wildfire environments.
"""

from .victim import Victim, VictimStatus
from .robot import Robot, RobotStatus
from .fire import FireSimulator, FirePredictor
from .astar import fire_aware_astar, standard_astar
from .swarm import SwarmPSOAllocator, greedy_allocation
from .environment import WildfireRescueEnv
from .simulation import SimulationEngine, SimulationResult

__all__ = [
    "Victim",
    "VictimStatus",
    "Robot",
    "RobotStatus",
    "FireSimulator",
    "FirePredictor",
    "fire_aware_astar",
    "standard_astar",
    "SwarmPSOAllocator",
    "greedy_allocation",
    "WildfireRescueEnv",
    "SimulationEngine",
    "SimulationResult",
]

