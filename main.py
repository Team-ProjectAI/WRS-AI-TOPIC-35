"""
Main Benchmark Script for Wildfire Rescue Swarm Intelligence Framework.
Evaluates 10 Test Scenarios under Baseline vs Proposed algorithms, prints a scientific comparison table,
and exports benchmark_results.csv.
"""

import json
import os
import sys
from typing import Dict, Any, List
import pandas as pd
import numpy as np

# Ensure root package can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.simulation import SimulationEngine, SimulationResult


def load_config(config_path: str = None) -> Dict[str, Any]:
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config", "default_config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_test_scenarios(scenarios_path: str = None) -> List[Dict[str, Any]]:
    if scenarios_path is None:
        scenarios_path = os.path.join(os.path.dirname(__file__), "data", "scenarios", "scenarios_test.json")
    with open(scenarios_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_benchmark(output_csv: str = "benchmark_results.csv"):
    config = load_config()
    scenarios = load_test_scenarios()

    print("=" * 80)
    print("🔥 WILDFIRE RESCUE SWARM INTELLIGENCE BENCHMARK SUITE")
    print("=" * 80)
    print(f"Loaded {len(scenarios)} Test Scenarios.")
    print("Modes evaluated: [1] Baseline (Greedy + Standard A*) vs [2] Proposed (PSO + Fire-Aware A* + U-Net)")
    print("-" * 80)

    results_data = []

    for i, sc in enumerate(scenarios, 1):
        sc_id = sc["id"]
        print(f"[{i:02d}/10] Running Scenario: {sc_id} (Seed: {sc['seed']})...")

        # 1. Baseline Run
        sim_base = SimulationEngine(config=config, scenario_data=sc, mode="baseline")
        res_base: SimulationResult = sim_base.run(record_frames=False)

        # 2. Proposed Run
        sim_prop = SimulationEngine(config=config, scenario_data=sc, mode="proposed")
        res_prop: SimulationResult = sim_prop.run(record_frames=False)

        results_data.append(res_base.to_dict())
        results_data.append(res_prop.to_dict())

    df = pd.DataFrame(results_data)

    # Save to CSV
    csv_path = os.path.join(os.path.dirname(__file__), output_csv)
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Benchmark results exported to: {csv_path}\n")

    # Summary Statistics Grouped by Mode
    summary_cols = [
        "rescue_success_rate",
        "total_distance",
        "fire_risk_exposure",
        "execution_time_steps",
        "replanning_count",
    ]

    base_df = df[df["mode"] == "baseline"]
    prop_df = df[df["mode"] == "proposed"]

    base_mean = base_df[summary_cols].mean()
    prop_mean = prop_df[summary_cols].mean()
    base_std = base_df[summary_cols].std()
    prop_std = prop_df[summary_cols].std()

    print("=" * 88)
    print("📊 SCIENTIFIC EVALUATION SUMMARY (MEAN ± STD OVER 10 TEST SCENARIOS)")
    print("=" * 88)
    print(f"{'Evaluation Metric':<28} | {'Baseline (Greedy+A*)':<24} | {'Proposed (PSO+U-Net A*)':<26} | {'Improvement'}")
    print("-" * 88)

    metrics_meta = [
        ("rescue_success_rate", "Rescue Success Rate (%)", True),
        ("total_distance", "Total Travel Distance (steps)", False),
        ("fire_risk_exposure", "Fire Risk Exposure (count)", False),
        ("execution_time_steps", "Execution Time (steps)", False),
        ("replanning_count", "Dynamic Replannings (count)", None),
    ]

    for key, label, higher_is_better in metrics_meta:
        b_val = base_mean[key]
        b_s = base_std[key]
        p_val = prop_mean[key]
        p_s = prop_std[key]

        b_str = f"{b_val:6.2f} ± {b_s:4.2f}"
        p_str = f"{p_val:6.2f} ± {p_s:4.2f}"

        if higher_is_better is True:
            diff = ((p_val - b_val) / (b_val + 1e-6)) * 100.0
            imp_str = f"{diff:+6.1f}%" if diff >= 0 else f"{diff:6.1f}%"
        elif higher_is_better is False:
            diff = ((b_val - p_val) / (b_val + 1e-6)) * 100.0
            imp_str = f"{diff:+6.1f}% (reduced)"
        else:
            imp_str = f"{p_val - b_val:+6.1f} (adaptive)"

        print(f"{label:<28} | {b_str:<24} | {p_str:<26} | {imp_str}")

    print("=" * 88)
    return df


if __name__ == "__main__":
    run_benchmark()

