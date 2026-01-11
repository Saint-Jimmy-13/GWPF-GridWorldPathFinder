from unified_planning.shortcuts import *
from unified_planning.io import PDDLReader
import os
from typing import List, Optional

def generate_pddl_problem(problem, output_filename: str = "problem.pddl") -> str:
    """
    problem: An instance of GridProblem class
    output_filename: Where to save the PDDL string
    """

    # Helper to name cells
    def get_cell_name(r, c):
        return f"cell_{r}_{c}"
    
    lines = []
    lines.append("(define (problem grid-problem-1)")
    lines.append("  (:domain grid-pathfinding)")
    lines.append("  (:objects")

    # 1. Define Objects (only non-obstacle cells)
    cells = []
    for r in range(problem.size):
        for c in range(problem.size):
            if (r, c) not in problem.obstacles:
                cells.append(get_cell_name(r, c))
    lines.append("    " + " ".join(cells) + " - location")
    lines.append("  )")

    lines.append("  (:init")
    # 2. Initial State
    start_r, start_c = problem.start
    lines.append(f"    (at {get_cell_name(start_r, start_c)})")

    # 3. Connectivity (Graph edges)
    # We iterate through all valid cells and check their neighbors
    for r in range(problem.size):
        for c in range(problem.size):
            if (r, c) in problem.obstacles:
                continue

            # Check all 4 directions
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                # If neighbor is within bounds and not wall
                if 0 <= nr < problem.size and 0 <= nc < problem.size:
                    if (nr, nc) not in problem.obstacles:
                        lines.append(f"   (connected {get_cell_name(r, c)} {get_cell_name(nr, nc)})")
    lines.append("  )")

    lines.append("  (:goal")
    goal_r, goal_c = problem.goal
    lines.append(f"    (at {get_cell_name(goal_r, goal_c)})")
    lines.append("  )")
    lines.append(")")

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Write to file
    with open(output_filename, "w") as f:
        f.write("\n".join(lines))
    return output_filename

def run_planning_solver(domain_file: str, problem_file: str) -> Optional[List[str]]:
    """
    Solves the PDDL problem using unified-planning.
    Returns: A list of actions (the plan) or None if failed.
    """
    # 1. Parse the PDDL files
    reader = PDDLReader()
    try:
        pddl_problem = reader.parse_problem(domain_file, problem_file)
    except Exception as e:
        print(f"Error parsing PDDL: {e}")
        return None
    
    # 2. Call the Solver
    # 'name' can be specific (e.g., 'pyperplan', 'fast-downward') or omitted to let UP pick one.
    # 'pyperplan' is used here as it installs easily via pip for testing.
    with OneshotPlanner(name='pyperplan') as planner:
        result = planner.solve(pddl_problem)

        # 3. Parse Output and Reconstruct Solution
        if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
            # result.plan is a unified_planning object. It is converted to a list of strings.
            # The plan actions usually look like "move(cell_0_0, cell_0_1)"
            return [str(a) for a in result.plan.actions]
        print("No solution found by planner.")
        return None
