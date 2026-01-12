# AI Homework: Grid Pathfinding & Planning

This repository implements an AI pipeline for the **Grid Pathfinding** problem. It compares specialized search algorithms against general-purpose automated planners.

**Project Scope:**
1.  **Task 1 (Problem):** A Grid World environment with random obstacles.
2.  **Task 2.1 (A\* Search):** Custom implementation supporting:
    * *Manhattan Distance* (Admissible, consistent).
    * *Euclidean Distance* (Admissible, consistent, but less informed).
3.  **Task 2.2 (Automated Planning):** PDDL modeling solved via:
    * *Pyperplan* (Heuristic-based Python planner).
    * *Fast Downward* (High-performance C++ planner).

Developed for the **Artificial Intelligence (2025-26)** course at Sapienza University.

## 📂 Project Structure

* `grid_problem.py`: Problem definition and A* implementation.
* `planning_utils.py`: PDDL generation and solver integration.
* `experiments.py`: Main script to run benchmarks (loops through all algorithms).
* `plot_results.py`: Generates graphs from the CSV results.
* `domain.pddl`: Grid pathfinding PDDL domain.
* `visualizer.py`: Visualizes the grid, obstacles, and the path found in png images.
* `output/`: Generated during runtime (contains logs, CSVs, images, PDDL problems).

## 🛠️ Installation

1.  **Create Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### ⚠️ Note on Fast Downward
The **Fast Downward** planner is a C++ engine. It installs easily on **Linux, macOS, and WSL** (Windows Subsystem for Linux).
* **If you are on native Windows:** The installation might fail or the planner might not run. The code is designed to skip Fast Downward gracefully if it fails, defaulting to Pyperplan only.

## 🚀 How to Run

1.  **Run Experiments:**
    This runs the benchmark loop (Grid sizes 5, 10, 15, 20, 25), creates the `output/` directory, and saves results.
    ```bash
    python experiments.py
    ```

2.  **Plot Results:**
    After experiments finish, generate the plots:
    ```bash
    python plot_results.py
    ```
    Check the `output/` folder for:
    ###### Performance Metrics
    * **`experiment_results.csv`**: Complete raw dataset of all runs.
    * **`plot_time.png`**: Execution Time vs Grid Size (Log Scale). Shows A* vs Planners.
    * **`plot_astar_expanded.png`**: Number of nodes expanded by A* (Manhattan vs Euclidean).
    * **`plot_astar_generated.png`**: Total number of nodes generated (children created) by A*.
    * **`plot_memory_nodes.png`**: Max abstract nodes kept in memory (Frontier + Explored).
    * **`plot_memory_mb.png`**: Peak physical memory usage in MB.
    * **`plot_branching.png`**: Average effective branching factor for A*.

    ###### Visualizations
    * **`vis_astar_<N>.png`**: A* solution path for grid size $N$ (e.g., `vis_astar_25.png`).
    * **`vis_plan_<N>.png`**: Planner (PDDL) solution path for grid size $N$ (e.g., `vis_plan_25.png`).
