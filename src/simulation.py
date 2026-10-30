"""
Simulation Engine for Wildfire Rescue Swarm.
Executes an episode under Baseline vs. Proposed framework, computing evaluation metrics
and capturing real-time simulation history for visualization.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set, Tuple
import numpy as np

from .victim import Victim, VictimStatus
from .robot import Robot, RobotStatus
from .fire import FireSimulator, FirePredictor
from .astar import standard_astar, fire_aware_astar
from .swarm import SwarmPSOAllocator, greedy_allocation


@dataclass
class SimulationResult:
    mode: str
    scenario_id: str
    rescue_success_rate: float  # Percentage [0 - 100%]
    total_distance: int          # Sum of grid steps across all robots
    fire_risk_exposure: int      # Count of robot steps in fire or hazardous risk zones
    execution_time_steps: int    # Number of steps until mission finished or timeout
    replanning_count: int        # Total replanning actions triggered
    num_victims: int
    rescued_count: int
    dead_count: int
    trapped_count: int
    frames: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "scenario_id": self.scenario_id,
            "rescue_success_rate": round(self.rescue_success_rate, 2),
            "total_distance": self.total_distance,
            "fire_risk_exposure": self.fire_risk_exposure,
            "execution_time_steps": self.execution_time_steps,
            "replanning_count": self.replanning_count,
            "num_victims": self.num_victims,
            "rescued_count": self.rescued_count,
            "dead_count": self.dead_count,
            "trapped_count": self.trapped_count,
        }


class SimulationEngine:
    """Executes a full multi-agent search and rescue mission."""

    def __init__(
        self,
        config: Dict[str, Any],
        scenario_data: Dict[str, Any],
        mode: str = "proposed",
    ):
        self.config = config
        self.scenario = scenario_data
        self.mode = mode.lower()
        self.scenario_id = scenario_data.get("id", "scenario_0")

        grid_size = scenario_data.get("grid_size", config.get("grid_size", [20, 20]))
        self.rows, self.cols = grid_size[0], grid_size[1]
        self.grid_shape = (self.rows, self.cols)

        self.max_steps = scenario_data.get("max_steps", config.get("max_steps", 80))
        self.seed = scenario_data.get("seed", config.get("seed", 42))

        # Obstacles & Fire setup
        self.obstacles: Set[Tuple[int, int]] = {
            tuple(o) for o in scenario_data.get("obstacles", [])
        }
        initial_fires = [tuple(f) for f in scenario_data.get("initial_fires", [])]
        wind_dir = tuple(scenario_data.get("wind_direction", config.get("wind_direction", [1.0, 0.0])))
        wind_speed = float(scenario_data.get("wind_speed", config.get("wind_speed", 1.0)))

        self.fire_sim = FireSimulator(
            rows=self.rows,
            cols=self.cols,
            initial_fires=initial_fires,
            obstacles=list(self.obstacles),
            base_spread_prob=float(scenario_data.get("fire_spread_prob", config.get("fire_spread_prob", 0.25))),
            wind_direction=wind_dir,
            wind_speed=wind_speed,
            seed=self.seed,
        )
        self.fire_predictor = FirePredictor()

        # Robots & Victims setup
        self.robots: List[Robot] = [
            Robot(id=r["id"], position=tuple(r["position"]))
            for r in scenario_data.get("robots", [])
        ]
        self.victims: List[Victim] = [
            Victim.from_dict(v) for v in scenario_data.get("victims", [])
        ]

        pso_cfg = config.get("pso", {})
        self.pso_allocator = SwarmPSOAllocator(
            pop_size=pso_cfg.get("pop_size", 30),
            max_gen=pso_cfg.get("max_gen", 35),
            seed=self.seed,
        )

        self.risk_weight = float(config.get("risk_weight", 8.0))
        self.safety_buffer_radius = int(config.get("safety_buffer_radius", 2))

    def run(self, record_frames: bool = True) -> SimulationResult:
        step = 0
        frames = []

        # Initial risk map
        risk_map = self._get_risk_map()

        # Initial task allocation
        self._allocate_tasks(risk_map)
        self._plan_initial_paths(risk_map)

        if record_frames:
            frames.append(self._capture_frame(step, risk_map))

        while step < self.max_steps:
            step += 1

            # 1. Fire Propagation
            self.fire_sim.step()
            burning_cells = set(self.fire_sim.get_burning_cells())

            # 2. Update Risk Heatmap
            risk_map = self._get_risk_map()

            # 3. Victims Status & Decay
            for v in self.victims:
                v.step_decay(in_fire=(v.position in burning_cells))

            # 4. Check Replanning / Reallocation Requirements
            needs_reallocation = False
            for robot in self.robots:
                # Check if robot's target is dead or trapped
                curr_target = self._get_victim(robot.current_target_id)
                if curr_target is None or not curr_target.is_active:
                    needs_reallocation = True
                    robot.current_target_id = None
                    robot.path = []
                    robot.status = RobotStatus.IDLE

                # Check if path is compromised by newly ignited fire
                elif robot.should_replan(burning_cells, risk_map if self.mode == "proposed" else None):
                    robot.replanning_count += 1
                    ok = robot.plan_path(
                        goal=curr_target.position,
                        grid_shape=self.grid_shape,
                        obstacles=self.obstacles,
                        fires=burning_cells,
                        mode=self.mode,
                        risk_map=risk_map,
                        risk_weight=self.risk_weight,
                        safety_buffer_radius=self.safety_buffer_radius,
                    )
                    if not ok:
                        # Target unreachable, request reallocation
                        needs_reallocation = True

            # 5. Dynamic Reallocation
            if needs_reallocation:
                active_victims = [v for v in self.victims if v.is_active]
                idle_or_blocked = [r for r in self.robots if r.status in (RobotStatus.IDLE, RobotStatus.BLOCKED)]
                if active_victims and idle_or_blocked:
                    self._allocate_tasks(risk_map)
                    for r in idle_or_blocked:
                        tgt = self._get_victim(r.current_target_id)
                        if tgt and tgt.is_active:
                            r.plan_path(
                                goal=tgt.position,
                                grid_shape=self.grid_shape,
                                obstacles=self.obstacles,
                                fires=burning_cells,
                                mode=self.mode,
                                risk_map=risk_map,
                                risk_weight=self.risk_weight,
                                safety_buffer_radius=self.safety_buffer_radius,
                            )

            # 6. Execute Robot Steps & Rescue Actions
            for robot in self.robots:
                target = self._get_victim(robot.current_target_id)
                if target and target.is_active and robot.position == target.position:
                    # At victim site -> perform rescue
                    robot.status = RobotStatus.RESCUING
                    robot.rescuing_timer += 1
                    if robot.rescuing_timer >= target.rescue_duration:
                        target.mark_rescued()
                        robot.pop_next_target()
                        next_tgt = self._get_victim(robot.current_target_id)
                        if next_tgt and next_tgt.is_active:
                            robot.plan_path(
                                goal=next_tgt.position,
                                grid_shape=self.grid_shape,
                                obstacles=self.obstacles,
                                fires=burning_cells,
                                mode=self.mode,
                                risk_map=risk_map,
                                risk_weight=self.risk_weight,
                                safety_buffer_radius=self.safety_buffer_radius,
                            )
                else:
                    if robot.path:
                        robot.step_move(burning_cells, risk_map)
                    elif target and target.is_active:
                        # Attempt to path towards target
                        robot.plan_path(
                            goal=target.position,
                            grid_shape=self.grid_shape,
                            obstacles=self.obstacles,
                            fires=burning_cells,
                            mode=self.mode,
                            risk_map=risk_map,
                            risk_weight=self.risk_weight,
                            safety_buffer_radius=self.safety_buffer_radius,
                        )
                        if robot.path:
                            robot.step_move(burning_cells, risk_map)
                    elif not target or not target.is_active:
                        # Try to pop next victim if available
                        robot.pop_next_target()
                        next_tgt = self._get_victim(robot.current_target_id)
                        if next_tgt and next_tgt.is_active:
                            robot.plan_path(
                                goal=next_tgt.position,
                                grid_shape=self.grid_shape,
                                obstacles=self.obstacles,
                                fires=burning_cells,
                                mode=self.mode,
                                risk_map=risk_map,
                                risk_weight=self.risk_weight,
                                safety_buffer_radius=self.safety_buffer_radius,
                            )

            if record_frames:
                frames.append(self._capture_frame(step, risk_map))

            # 7. Check Mission Termination
            active_remaining = [v for v in self.victims if v.is_active]
            if len(active_remaining) == 0:
                break

        # Compute Final Metrics
        total_dist = sum(r.total_distance for r in self.robots)
        total_risk = sum(r.fire_risk_exposure for r in self.robots)
        total_replans = sum(r.replanning_count for r in self.robots)

        rescued = sum(1 for v in self.victims if v.status == VictimStatus.RESCUED)
        dead = sum(1 for v in self.victims if v.status == VictimStatus.DEAD)
        trapped = sum(1 for v in self.victims if v.status == VictimStatus.TRAPPED)

        success_rate = (rescued / len(self.victims) * 100.0) if self.victims else 0.0

        return SimulationResult(
            mode=self.mode,
            scenario_id=self.scenario_id,
            rescue_success_rate=success_rate,
            total_distance=total_dist,
            fire_risk_exposure=total_risk,
            execution_time_steps=step,
            replanning_count=total_replans,
            num_victims=len(self.victims),
            rescued_count=rescued,
            dead_count=dead,
            trapped_count=trapped,
            frames=frames,
        )

    def _get_victim(self, victim_id: Optional[int]) -> Optional[Victim]:
        if victim_id is None:
            return None
        for v in self.victims:
            if v.id == victim_id:
                return v
        return None

    def _get_risk_map(self) -> np.ndarray:
        if self.mode == "proposed":
            return self.fire_predictor.predict_risk_map(
                fire_grid=self.fire_sim.fire_grid,
                fuel_grid=self.fire_sim.fuel_grid,
                wind_direction=self.fire_sim.wind_direction,
                wind_speed=self.fire_sim.wind_speed,
            )
        return np.zeros(self.grid_shape, dtype=np.float32)

    def _allocate_tasks(self, risk_map: np.ndarray):
        active_victims = [v for v in self.victims if v.is_active]
        if not active_victims or not self.robots:
            return

        if self.mode == "proposed":
            assignments = self.pso_allocator.allocate(
                robots=self.robots,
                victims=active_victims,
                risk_map=risk_map,
                weights=self.config.get("weights"),
            )
        else:
            assignments = greedy_allocation(
                robots=self.robots,
                victims=active_victims,
            )

        # Update robot target queues
        robot_queues = {r.id: [] for r in self.robots}
        for v_id, r_id in assignments.items():
            if r_id is not None and r_id in robot_queues:
                robot_queues[r_id].append(v_id)

        for robot in self.robots:
            v_list = [self._get_victim(vid) for vid in robot_queues.get(robot.id, []) if self._get_victim(vid)]
            if self.mode == "proposed":
                # Proposed: Prioritize critical victims and consider safety
                v_list.sort(key=lambda v: (-v.priority, abs(robot.x - v.x) + abs(robot.y - v.y)))
            else:
                # Baseline: Pure distance ordering
                v_list.sort(key=lambda v: abs(robot.x - v.x) + abs(robot.y - v.y))
            robot.set_queue([v.id for v in v_list])

    def _plan_initial_paths(self, risk_map: np.ndarray):
        fires = set(self.fire_sim.get_burning_cells())
        for robot in self.robots:
            target = self._get_victim(robot.current_target_id)
            if target:
                robot.plan_path(
                    goal=target.position,
                    grid_shape=self.grid_shape,
                    obstacles=self.obstacles,
                    fires=fires,
                    mode=self.mode,
                    risk_map=risk_map,
                    risk_weight=self.risk_weight,
                    safety_buffer_radius=self.safety_buffer_radius,
                )

    def _capture_frame(self, step: int, risk_map: np.ndarray) -> Dict[str, Any]:
        return {
            "step": step,
            "fire_grid": self.fire_sim.fire_grid.tolist(),
            "risk_map": risk_map.tolist(),
            "obstacles": [list(o) for o in self.obstacles],
            "robots": [r.to_dict() for r in self.robots],
            "victims": [v.to_dict() for v in self.victims],
        }
