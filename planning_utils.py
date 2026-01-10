"""
Planning utilities for PDDL problem generation and solving.
Integrates with unified_planning framework to solve grid pathfinding problems.
"""

import os
from pathlib import Path

try:
    from unified_planning.shortcuts import *
    from unified_planning.io import PDDLReader
except ImportError:
    print("ERROR: unified-planning not installed. Install with:")
    print("  pip install unified-planning pyperplan")
    raise

def generate_pddl_problem(problem, output_filename="problem.pddl"):
    """
    Generate a PDDL problem file from a GridProblem instance.
    
    The PDDL problem file defines:
    - Objects: All non-obstacle cells as locations
    - Initial state: Robot at start position
    - Connectivity: Edges between adjacent non-obstacle cells
    - Goal: Robot at goal position
    
    Args:
        problem: An instance of GridProblem class
        output_filename: Where to save the PDDL string
        
    Returns:
        str: Path to the created PDDL problem file
    """

    def get_cell_name(r, c):
        """Helper to name cells consistently."""
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
    
    # Format objects nicely in PDDL
    lines.append("    " + " ".join(cells) + " - location")
    lines.append("  )")

    lines.append("  (:init")

    # 2. Initial State: Robot at start position
    start_r, start_c = problem.start
    lines.append(f"    (at {get_cell_name(start_r, start_c)})")

    # 3. Connectivity: Define edges between adjacent non-obstacle cells
    # We iterate through all valid cells and check their 4-connected neighbors
    for r in range(problem.size):
        for c in range(problem.size):
            if (r, c) in problem.obstacles:
                continue

            # Check all 4 directions (up, down, left, right)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc

                # If neighbor is within bounds and not an obstacle
                if 0 <= nr < problem.size and 0 <= nc < problem.size:
                    if (nr, nc) not in problem.obstacles:
                        lines.append(
                            f"    (connected {get_cell_name(r, c)} {get_cell_name(nr, nc)})"
                        )
    
    lines.append("  )")

    # 4. Goal State: Robot at goal position
    lines.append("  (:goal")
    goal_r, goal_c = problem.goal
    lines.append(f"    (at {get_cell_name(goal_r, goal_c)})")
    lines.append("  )")

    lines.append(")")

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename) if os.path.dirname(output_filename) else ".", 
                exist_ok=True)
    
    # Write to file
    with open(output_filename, "w") as f:
        f.write("\n".join(lines))
    
    print(f"  Generated PDDL problem: {output_filename} ({len(cells)} cells)")
    
    return output_filename

def run_planning_solver(domain_file, problem_file):
    """
    Solves the PDDL problem using unified-planning with pyperplan backend.
    
    Args:
        domain_file: Path to PDDL domain file
        problem_file: Path to PDDL problem file
        
    Returns:
        list: A list of action strings (the plan) like ["move(cell_0_0, cell_0_1)", ...]
              or None if no solution was found
    """

    # Verify files exist
    if not os.path.exists(domain_file):
        print(f"  ERROR: Domain file '{domain_file}' not found")
        return None
    
    if not os.path.exists(problem_file):
        print(f"  ERROR: Problem file '{problem_file}' not found")
        return None

    # 1. Parse the PDDL files
    reader = PDDLReader()

    try:
        pddl_problem = reader.parse_problem(domain_file, problem_file)
    except Exception as e:
        print(f"  ERROR parsing PDDL: {e}")
        return None
    
    # 2. Call the Solver (pyperplan is lightweight and installs easily)
    try:
        with OneshotPlanner(name='pyperplan') as planner:
            result = planner.solve(pddl_problem)
    except Exception as e:
        print(f"  ERROR invoking planner: {e}")
        return None

    # 3. Parse Output and Reconstruct Solution
    try:
        # Check if solution was found
        import unified_planning as up
        
        if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
            # Convert plan actions to string representation
            plan_list = [str(a) for a in result.plan.actions]
            return plan_list
        else:
            print(f"  Planner status: {result.status}")
            return None
    except Exception as e:
        print(f"  ERROR reconstructing plan: {e}")
        return None
