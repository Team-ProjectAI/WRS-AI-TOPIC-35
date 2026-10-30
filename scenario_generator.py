"""
Scenario Generator for Wildfire Rescue Swarm Intelligence Framework.
Generates 30 reproducible, standardized scenarios partitioned into:
- scenarios_dev.json (10 scenarios)
- scenarios_val.json (10 scenarios)
- scenarios_test.json (10 scenarios)
"""

import json
import os
from typing import Dict, Any, List
import numpy as np


def generate_single_scenario(scenario_id: str, seed: int, grid_size: int = 20) -> Dict[str, Any]:
    rng = np.random.RandomState(seed)

    # Wind setup
    angle = rng.uniform(0, 2 * np.pi)
    wind_speed = round(float(rng.uniform(0.8, 2.2)), 2)
    wind_dir = [round(float(np.cos(angle)), 3), round(float(np.sin(angle)), 3)]

    # Fire spread probability
    fire_prob = round(float(rng.uniform(0.20, 0.35)), 2)

    # Obstacles (~6% of grid)
    num_obstacles = int(grid_size * grid_size * 0.06)
    obstacles = set()
    while len(obstacles) < num_obstacles:
        ox = int(rng.randint(2, grid_size - 2))
        oy = int(rng.randint(2, grid_size - 2))
        obstacles.add((ox, oy))

    # Initial fire ignition clusters (1 to 3 clusters)
    initial_fires = set()
    num_clusters = rng.randint(1, 3)
    for _ in range(num_clusters):
        cx = int(rng.randint(grid_size // 4, 3 * grid_size // 4))
        cy = int(rng.randint(grid_size // 4, 3 * grid_size // 4))
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (cx + dx, cy + dy) not in obstacles and 0 <= cx + dx < grid_size and 0 <= cy + dy < grid_size:
                    if rng.rand() < 0.6:
                        initial_fires.add((cx + dx, cy + dy))
    if not initial_fires:
        initial_fires.add((grid_size // 2, grid_size // 2))

    # Robot starting fleet (3 robots along western border)
    num_robots = 3
    robots = []
    for i in range(num_robots):
        ry = int(i * (grid_size // num_robots) + 1)
        rx = 0
        robots.append({"id": i, "position": [rx, ry]})

    # Victims (5 to 7 victims distributed in forest)
    num_victims = rng.randint(5, 8)
    victims = []
    used_positions = set(obstacles).union(initial_fires)
    for r in robots:
        used_positions.add(tuple(r["position"]))

    for v_id in range(num_victims):
        vx = int(rng.randint(grid_size // 3, grid_size))
        vy = int(rng.randint(0, grid_size))
        while (vx, vy) in used_positions:
            vx = int(rng.randint(1, grid_size))
            vy = int(rng.randint(0, grid_size))
        used_positions.add((vx, vy))

        priority = int(rng.choice([1, 2, 3], p=[0.4, 0.35, 0.25]))
        max_wait = int(rng.randint(60, 110))
        victims.append({
            "id": v_id,
            "position": [vx, vy],
            "priority": priority,
            "max_wait_time": max_wait,
            "rescue_duration": 1,
        })

    return {
        "id": scenario_id,
        "seed": seed,
        "grid_size": [grid_size, grid_size],
        "max_steps": 80,
        "fire_spread_prob": fire_prob,
        "wind_direction": wind_dir,
        "wind_speed": wind_speed,
        "obstacles": [list(o) for o in obstacles],
        "initial_fires": [list(f) for f in initial_fires],
        "robots": robots,
        "victims": victims,
    }


def generate_all_scenarios(base_dir: str = None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    out_dir = os.path.join(base_dir, "data", "scenarios")
    os.makedirs(out_dir, exist_ok=True)

    splits = {
        "scenarios_dev.json": (0, 10, 100),
        "scenarios_val.json": (10, 20, 200),
        "scenarios_test.json": (20, 30, 300),
    }

    for filename, (start_idx, end_idx, seed_offset) in splits.items():
        scenario_list = []
        for i in range(start_idx, end_idx):
            sid = f"scenario_{i+1:02d}"
            sc = generate_single_scenario(sid, seed=seed_offset + i)
            scenario_list.append(sc)

        filepath = os.path.join(out_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(scenario_list, f, indent=2)
        print(f"Generated {len(scenario_list)} scenarios -> {filepath}")


if __name__ == "__main__":
    generate_all_scenarios()
