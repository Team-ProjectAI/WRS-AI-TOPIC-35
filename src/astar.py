"""
A* Pathfinding Algorithms:
1. Standard A* (baseline): Pure distance-based search.
2. Fire-Aware A* (proposed): Distance + U-Net fire spread risk penalty.
"""

import heapq
import math
from typing import List, Tuple, Set, Optional, Dict
import numpy as np


def get_neighbors(x: int, y: int, rows: int, cols: int, allow_diagonal: bool = False):
    """4-directional or 8-directional movement."""
    if allow_diagonal:
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in deltas:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows:
            yield (nx, ny), math.hypot(dx, dy)


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """Manhattan distance heuristic."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def standard_astar(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    grid_shape: Tuple[int, int],
    obstacles: Set[Tuple[int, int]],
    fires: Set[Tuple[int, int]],
) -> Optional[List[Tuple[int, int]]]:
    """
    Baseline Standard A*: Treats active fires and obstacles as untraversable.
    Only minimizes total path distance.
    """
    rows, cols = grid_shape
    blocked = obstacles.union(fires)

    if start in blocked or goal in blocked:
        # If goal is blocked by fire, cannot reach
        return None
    if start == goal:
        return [start]

    open_set = []
    heapq.heappush(open_set, (0.0, start))
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], float] = {start: 0.0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor, move_cost in get_neighbors(current[0], current[1], rows, cols):
            if neighbor in blocked:
                continue

            tentative_g = g_score[current] + move_cost
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None


def fire_aware_astar(
    start: Tuple[int, int],
    goal: Tuple[int, int],
    grid_shape: Tuple[int, int],
    obstacles: Set[Tuple[int, int]],
    fires: Set[Tuple[int, int]],
    risk_map: np.ndarray,
    risk_weight: float = 8.0,
    safety_buffer_radius: int = 1,
) -> Optional[List[Tuple[int, int]]]:
    """
    Proposed Fire-Aware A*:
    Balances step length and fire ignition risk predicted by U-Net.
    cost(u -> v) = move_cost + risk_weight * risk_map[v] + buffer_penalty
    """
    rows, cols = grid_shape
    blocked = obstacles.union(fires)

    if start == goal:
        return [start]
    if goal in blocked:
        return None

    # Safety buffer penalty calculation
    buffer_cells: Dict[Tuple[int, int], float] = {}
    if safety_buffer_radius > 0:
        for fx, fy in fires:
            for dy in range(-safety_buffer_radius, safety_buffer_radius + 1):
                for dx in range(-safety_buffer_radius, safety_buffer_radius + 1):
                    dist = abs(dx) + abs(dy)
                    if 0 < dist <= safety_buffer_radius:
                        bx, by = fx + dx, fy + dy
                        if 0 <= bx < cols and 0 <= by < rows and (bx, by) not in blocked:
                            penalty = (safety_buffer_radius - dist + 1) * 3.0
                            buffer_cells[(bx, by)] = max(buffer_cells.get((bx, by), 0.0), penalty)

    open_set = []
    heapq.heappush(open_set, (0.0, start))
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], float] = {start: 0.0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor, move_cost in get_neighbors(current[0], current[1], rows, cols):
            if neighbor in blocked:
                continue

            nx, ny = neighbor
            cell_risk = float(risk_map[ny, nx]) if 0 <= ny < rows and 0 <= nx < cols else 0.0
            buf_cost = buffer_cells.get(neighbor, 0.0)

            # Combined risk-aware traversal cost
            edge_cost = move_cost + (risk_weight * cell_risk) + buf_cost
            tentative_g = g_score[current] + edge_cost

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None

