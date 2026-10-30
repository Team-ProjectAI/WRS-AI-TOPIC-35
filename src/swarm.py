"""
Swarm Allocation Algorithms:
1. Greedy Allocation (Baseline): Robots independently choose closest active victim.
2. PSO Swarm Allocation (Proposed): Multi-agent Task Allocation formulated as an
   optimization problem solved with pymoo Particle Swarm Optimization (PSO).
"""

from typing import List, Dict, Optional, Tuple, Set
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.optimize import minimize

from .victim import Victim, VictimStatus
from .robot import Robot


class SwarmTaskAllocationProblem(ElementwiseProblem):
    """
    Formulates Swarm Allocation:
    - n_var = number of active victims
    - Each variable x_i in [0, num_robots - 1] (discrete index of assigned robot)
    - Objective: Minimize total travel distance, priority-weighted delay penalty, and workload disparity.
    """

    def __init__(
        self,
        robots: List[Robot],
        victims: List[Victim],
        risk_map: Optional[np.ndarray] = None,
        weights: Optional[Dict[str, float]] = None,
    ):
        self.robots = robots
        self.victims = victims
        self.risk_map = risk_map
        self.weights = weights or {"distance": 1.0, "priority": 3.0, "risk": 4.0, "balance": 2.0}

        n_var = len(victims)
        n_robots = len(robots)

        super().__init__(
            n_var=n_var,
            n_obj=1,
            n_ieq_constr=0,
            xl=np.zeros(n_var),
            xu=np.full(n_var, n_robots - 1),
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Round continuous particle positions to robot indices
        assignments = np.clip(np.round(x).astype(int), 0, len(self.robots) - 1)

        total_cost = 0.0
        robot_workloads = [0 for _ in self.robots]

        for v_idx, r_idx in enumerate(assignments):
            robot = self.robots[r_idx]
            victim = self.victims[v_idx]

            # Distance cost (Manhattan)
            dist = abs(robot.x - victim.x) + abs(robot.y - victim.y)
            robot_workloads[r_idx] += dist

            # Priority penalty: high priority victims (e.g. priority 3) penalized if distant
            priority_penalty = (4 - victim.priority) * 0.5 + (dist * (victim.priority * 0.8))

            # Fire risk around victim
            v_risk = 0.0
            if self.risk_map is not None:
                if 0 <= victim.y < self.risk_map.shape[0] and 0 <= victim.x < self.risk_map.shape[1]:
                    v_risk = float(self.risk_map[victim.y, victim.x])

            total_cost += (
                self.weights.get("distance", 1.0) * dist
                + self.weights.get("priority", 3.0) * priority_penalty
                + self.weights.get("risk", 4.0) * v_risk * 20.0
            )

        # Workload balance variance penalty
        if len(self.robots) > 1:
            variance = np.var(robot_workloads)
            total_cost += self.weights.get("balance", 2.0) * variance

        out["F"] = [total_cost]


class SwarmPSOAllocator:
    """PSO-based Swarm Optimizer for Victim Allocation."""

    def __init__(self, pop_size: int = 30, max_gen: int = 35, seed: int = 42):
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.seed = seed

    def allocate(
        self,
        robots: List[Robot],
        victims: List[Victim],
        risk_map: Optional[np.ndarray] = None,
        weights: Optional[Dict[str, float]] = None,
    ) -> Dict[int, Optional[int]]:
        """
        Runs PSO to assign active victims to robots.
        Returns: {victim_id: robot_id}
        """
        active_victims = [v for v in victims if v.is_active]
        if not active_victims or not robots:
            return {}

        # If only 1 victim or 1 robot, deterministic assignment
        if len(robots) == 1:
            return {v.id: robots[0].id for v in active_victims}

        problem = SwarmTaskAllocationProblem(
            robots=robots,
            victims=active_victims,
            risk_map=risk_map,
            weights=weights,
        )

        algorithm = PSO(
            pop_size=min(self.pop_size, max(10, len(active_victims) * 6)),
            seed=self.seed,
        )

        res = minimize(
            problem,
            algorithm,
            ("n_gen", self.max_gen),
            seed=self.seed,
            verbose=False,
        )

        best_x = np.clip(np.round(res.X).astype(int), 0, len(robots) - 1)
        assignment: Dict[int, Optional[int]] = {}
        for v_idx, r_idx in enumerate(best_x):
            assignment[active_victims[v_idx].id] = robots[r_idx].id

        return assignment


def greedy_allocation(
    robots: List[Robot],
    victims: List[Victim],
) -> Dict[int, Optional[int]]:
    """
    Baseline Greedy Allocation:
    Iterates through robots and picks the closest unassigned active victim.
    """
    active_victims = [v for v in victims if v.is_active]
    if not active_victims or not robots:
        return {}

    assigned_victim_ids: Set[int] = set()
    result: Dict[int, Optional[int]] = {}

    for robot in robots:
        best_v = None
        best_dist = float("inf")
        for v in active_victims:
            if v.id in assigned_victim_ids:
                continue
            dist = abs(robot.x - v.x) + abs(robot.y - v.y)
            if dist < best_dist:
                best_dist = dist
                best_v = v

        if best_v is not None:
            result[best_v.id] = robot.id
            assigned_victim_ids.add(best_v.id)

    # Assign remaining victims to closest robot
    for v in active_victims:
        if v.id not in assigned_victim_ids:
            closest_robot = min(robots, key=lambda r: abs(r.x - v.x) + abs(r.y - v.y))
            result[v.id] = closest_robot.id

    return result

