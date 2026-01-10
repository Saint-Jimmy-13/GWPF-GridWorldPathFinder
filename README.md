# AI Homework: Grid Pathfinding & Planning

This repository contains the implementation of an AI experimental pipeline for the **Grid Pathfinding** problem. It compares two distinct AI techniques:
1.  **A\* Search** (Custom implementation with Manhattan distance heuristic).
2.  **Automated Planning** (Modeled in PDDL and solved using the `unified-planning` library).

This project was developed for the **Artificial Intelligence (2025-26)** course at Sapienza University of Rome.

## 📂 Project Structure

* `grid_problem.py`: Contains the `GridProblem` class (Task 1) and the custom `a_star_search` implementation (Task 2.1).
* `planning_utils.py`: Functions to generate PDDL problem files and run the solver using `unified-planning` (Task 2.2).
* `experiments.py`: Main script that runs the benchmark experiments on increasing grid sizes (Task 3).
* `plot_results.py`: Generates graphs (Time, Memory, Nodes) from the experimental data.
* `domain.pddl`: The PDDL domain definition for the Grid World.
* `problems/`: Directory where generated PDDL problem files are stored.

## 🛠️ Dependencies

The project is written in **Python 3**. The following external libraries are required:

* **unified-planning**: For parsing and solving PDDL models.
* **pandas**: For data manipulation.
* **matplotlib**: For plotting experimental results.

### Installation
It is recommended to use a virtual environment.

```bash
# 1. Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 2. Install dependencies
pip install unified-planning[pyperplan] pandas matplotlib
