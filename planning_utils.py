from unified_planning.shortcuts import *
from unified_planning.io import PDDLReader
import os
from typing import List, Optional

def generate_pddl_problem(problem, output_filename: str = "problem.pddl") -> str:
    """ Generates PDDL problem file from GridProblem """
    def get_cell_name(r, c):
        return f"cell_{r}_{c}"
    
    lines = []
    lines.append("(define (problem grid-problem-1)")
    lines.append("  (:domain grid-pathfinding)")
    lines.append("  (:objects")

    cells = []
    for r in range(problem.size):
        for c in range(problem.size):
            if (r, c) not in problem.obstacles:
                cells.append(get_cell_name(r, c))
    lines.append("    " + " ".join(cells) + " - location")
    lines.append("  )")

    lines.append("  (:init")
    start_r, start_c = problem.start
    lines.append(f"    (at {get_cell_name(start_r, start_c)})")

    for r in range(problem.size):
        for c in range(problem.size):
            if (r, c) in problem.obstacles: continue
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < problem.size and 0 <= nc < problem.size:
                    if (nr, nc) not in problem.obstacles:
                        lines.append(f"   (connected {get_cell_name(r, c)} {get_cell_name(nr, nc)})")
    lines.append("  )")

    lines.append("  (:goal")
    goal_r, goal_c = problem.goal
    lines.append(f"    (at {get_cell_name(goal_r, goal_c)})")
    lines.append("  )")
    lines.append(")")

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, "w") as f:
        f.write("\n".join(lines))
    return output_filename

def run_planning_solver(domain_file: str, problem_file: str, planner_name: str = 'pyperplan') -> Optional[List[str]]:
    """
    Solves the PDDL problem using the specified planner engine.
    planner_name options: 'pyperplan', 'fast-downward', 'tarski', etc.
    """
    reader = PDDLReader()
    try:
        pddl_problem = reader.parse_problem(domain_file, problem_file)
    except Exception as e:
        print(f"Error parsing PDDL: {e}")
        return None
    
    try:
        with OneshotPlanner(name=planner_name) as planner:
            result = planner.solve(pddl_problem)
            if result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING:
                return [str(a) for a in result.plan.actions]
            elif result.status == up.engines.PlanGenerationResultStatus.SOLVED_OPTIMALLY:
                return [str(a) for a in result.plan.actions]
    except Exception as e:
        # Fallback error logging
        print(f"Planner '{planner_name}' failed: {e}")
        return None
        
    return None
