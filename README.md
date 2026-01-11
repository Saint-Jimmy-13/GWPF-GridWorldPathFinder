# AI Homework: Grid Pathfinding & Planning

This repository implements an AI pipeline for the **Grid Pathfinding** problem. It compares two techniques:
1.  **A\* Search**: Custom implementation with Manhattan distance (Task 2.1).
2.  **Automated Planning**: PDDL modeling solved via `pyperplan` (Task 2.2).

Developed for the **Artificial Intelligence (2025-26)** course at Sapienza University.

## 📂 Project Structure

* `grid_problem.py`: Problem definition and A* implementation.
* `planning_utils.py`: PDDL generation and solver integration.
* `experiments.py`: Main script to run benchmarks and save data to `output/`.
* `plot_results.py`: Generates graphs from the CSV results.
* `domain.pddl`: Grid pathfinding PDDL domain.
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

## 🚀 How to Run

1.  **Run Experiments:**
    This runs the benchmark loop (Grid sizes 5, 10, 15, 20), creates the `output/` directory, and saves results.
    ```bash
    python experiments.py
    ```

2.  **Plot Results:**
    After experiments finish, generate the plots:
    ```bash
    python plot_results.py
    ```
    Check the `output/` folder for `plot_time.png`, `plot_success_rate.png`, etc.
