# Wildfire Rescue Swarm Intelligence

A research-oriented simulation of multi-robot wildfire rescue in a dynamic, hazardous environment. The project compares a conventional greedy planner with a hybrid strategy that combines fire-aware A* pathfinding, particle swarm optimization (PSO) for task allocation, and an optional PyTorch U-Net fire-risk model.

> **Status:** Academic prototype for experimentation and benchmarking. It is not intended for direct deployment in emergency-response systems.

## Highlights

- Dynamic cellular-automata wildfire simulation with wind, obstacles, and changing risk.
- Multi-robot rescue coordination with victim priorities and survival deadlines.
- Baseline (`greedy + A*`) and proposed (`PSO + fire-aware A*`) planning modes.
- Optional U-Net inference and training pipeline for next-step fire-risk prediction.
- Reproducible development, validation, and test scenario splits.
- Streamlit dashboard for interactive simulation and result inspection.

## System architecture

1. **Fire-risk prediction** — `models/unet.py` defines the compact PyTorch U-Net used by the fire model when trained weights are available.
2. **Simulation environment** — `src/environment.py`, `src/fire.py`, `src/robot.py`, and `src/victim.py` model the grid, fire, robots, and victims.
3. **Task allocation** — `src/swarm.py` assigns victims to robots using the configured swarm optimizer.
4. **Path planning** — `src/astar.py` computes routes that account for fire risk and safety buffers.
5. **Experiment runner** — `src/simulation.py` coordinates each run; `main.py` compares both planning modes.

## Requirements

- Python 3.10–3.12
- 4 CPU cores and 8 GB RAM recommended
- NVIDIA GPU with CUDA is optional; the compact model can run on CPU

## Installation

```bash
git clone https://github.com/Team-ProjectAI/WRS-AI-TOPIC-35.git
cd WRS-AI-TOPIC-35/wildfire_rescue_swarm

python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Quick start

Run the reproducible benchmark over the checked-in test scenarios:

```bash
python main.py
```

The command evaluates the baseline and proposed modes and writes `benchmark_results.csv` in the project root.

Launch the interactive dashboard:

```bash
streamlit run app.py
```

Generate fresh scenario splits when required:

```bash
python scenario_generator.py
```

## Training the fire-risk model

The training script expects the wildfire data layout used by the project and writes model checkpoints to `models/` and training metrics to `logs/`:

```bash
python models/train_fire_unet.py
```

The application prefers `models/best_unet_fire.pth` and falls back to `models/wildfire_unet.pth` when available. Large raw datasets are intentionally excluded from version control; place them under `data/wildfire_raw/` locally.

## Configuration

Edit [`config/default_config.json`](config/default_config.json) to change grid size, simulation horizon, robot/victim counts, fire behavior, safety-buffer radius, objective weights, and PSO parameters. The benchmark loads this file automatically.

Scenario data is stored in [`data/scenarios/`](data/scenarios/):

- `scenarios_dev.json` — development scenarios
- `scenarios_val.json` — validation scenarios
- `scenarios_test.json` — benchmark scenarios

## Repository layout

```text
wildfire_rescue_swarm/
├── app.py                  # Streamlit dashboard
├── main.py                 # Benchmark entry point
├── scenario_generator.py   # Reproducible scenario generation
├── config/                 # Runtime configuration
├── data/scenarios/         # Checked-in scenario definitions
├── models/                 # U-Net implementation, training, and checkpoints
└── src/                    # Simulation, fire, robot, victim, swarm, and A*
```

Generated logs, caches, virtual environments, and raw datasets are ignored by Git. Presentation files, videos, and other course-delivery artifacts are intentionally kept outside the software repository.

## Evaluation metrics

The benchmark reports:

- Rescue success rate
- Total travel distance
- Fire-risk exposure
- Execution time in simulation steps
- Number of dynamic replans

Results are deterministic for a fixed configuration and scenario seed. They are intended for comparative research, not as a claim of field performance.

## Academic context

This repository was developed for HUTECH AI coursework (Topic 35). The implementation is provided for educational and research use. Please cite the repository and the underlying wildfire-spread dataset if you reuse the code or results.

## License

No license file is currently included. Add an explicit license before redistributing this project or incorporating it into another product.
