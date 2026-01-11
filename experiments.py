import time
import random
import csv
import os
import tracemalloc
from grid_problem import GridProblem, a_star_search
from planning_utils import generate_pddl_problem, run_planning_solver
from visualizer import draw_grid

# Heuristic for A* (Manhattan Distance)
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def run_experiments():
    # --- Configuration ---
    OUTPUT_DIR = "output"
    PROBLEMS_DIR = os.path.join(OUTPUT_DIR, "problems")
    
    # Scaling parameter: Grid sizes
    SIZES = [5, 10, 15, 20] 
    NUM_RUNS = 5
    RANDOM_SEED = 42

    # Ensure directories exist
    os.makedirs(PROBLEMS_DIR, exist_ok=True)
    
    # Set seed for reproducibility
    random.seed(RANDOM_SEED)

    results = []
    
    print(f"Starting Experiments... (Seed: {RANDOM_SEED})")
    print(f"{'Size':<5} | {'Run':<3} | {'Algo':<8} | {'Status':<10} | {'Time (s)':<8} | {'Nodes/Len':<10} | {'Path (First 3 steps)'}")
    print("-" * 90)

    for N in SIZES:
        for run_i in range(NUM_RUNS):
            # --- 1. Generate Random Instance ---
            obstacles = []
            for r in range(N):
                for c in range(N):
                    # 20% Obstacle density
                    if random.random() < 0.2:
                        obstacles.append((r, c))
            
            start, goal = (0, 0), (N - 1, N - 1)
            # Ensure start/goal are valid
            if start in obstacles: obstacles.remove(start)
            if goal in obstacles: obstacles.remove(goal)
            
            problem = GridProblem(N, start, goal, obstacles)

            # --- 2. Run A* ---
            tracemalloc.start()
            start_time = time.time()
            
            path_a_star, node_count, avg_bf, max_bf = a_star_search(problem, manhattan_distance)
            
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            a_star_mem = peak / 10**6  # Convert Bytes to MB
            tracemalloc.stop()

            a_star_time = end_time - start_time
            success_a = True if path_a_star else False
            path_str = str(path_a_star[:3]) + "..." if path_a_star else "None"

            print(f"{N:<5} | {run_i:<3} | {'A*':<8} | {'[SUCCESS]' if success_a else '[FAILURE]':<10} | {a_star_time:<8.4f} | {node_count:<10} | {path_str}")

            # Save visual of the first run of each size
            if run_i == 0 and success_a:
                draw_grid(problem, path_a_star, "A*", os.path.join(OUTPUT_DIR, f"vis_astar_{N}.png"))

            results.append({
                'Size': N, 'Run': run_i, 'Algorithm': 'A*',
                'Success': success_a, 'Time': a_star_time, 
                'Metric_Value': node_count, 'Memory_MB': a_star_mem,
                'Avg_Branching': avg_bf, 'Max_Branching': max_bf
            })

            # --- 3. Run Planner ---
            domain_file = "domain.pddl"
            prob_file_path = os.path.join(PROBLEMS_DIR, f"prob_{N}_{run_i}.pddl")
            generate_pddl_problem(problem, prob_file_path)

            tracemalloc.start()
            start_time = time.time()
            
            try:
                plan = run_planning_solver(domain_file, prob_file_path)
            except Exception as e:
                plan = None
                print(f"Planner Error: {e}")

            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            planner_mem = peak / 10**6
            tracemalloc.stop()

            planner_time = end_time - start_time
            success_p = True if plan else False
            plan_len = len(plan) if plan else 0
            plan_str = str(plan[:3]) + "..." if plan else "None"

            print(f"{N:<5} | {run_i:<3} | {'Planner':<8} | {'[SUCCESS]' if success_p else '[FAILURE]':<10} | {planner_time:<8.4f} | {plan_len:<10} | {plan_str}")

            if run_i == 0 and success_p:
                draw_grid(problem, plan, "Planner", os.path.join(OUTPUT_DIR, f"vis_plan_{N}.png"))

            results.append({
                'Size': N, 'Run': run_i, 'Algorithm': 'Planner',
                'Success': success_p, 'Time': planner_time,
                'Metric_Value': plan_len, 'Memory_MB': planner_mem,
                'Avg_Branching': 0, 'Max_Branching': 0
            })

    # --- 4. Save to CSV ---
    csv_path = os.path.join(OUTPUT_DIR, 'experiment_results.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nExperiments completed. Results saved to '{csv_path}'.")

if __name__ == "__main__":
    run_experiments()
