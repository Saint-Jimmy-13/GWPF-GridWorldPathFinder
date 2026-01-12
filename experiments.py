import time
import random
import csv
import os
import math
import tracemalloc
from grid_problem import GridProblem, a_star_search
from planning_utils import generate_pddl_problem, run_planning_solver
from visualizer import draw_grid

# --- Heuristics ---
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def run_experiments():
    # --- Configuration ---
    OUTPUT_DIR = "output"
    PROBLEMS_DIR = os.path.join(OUTPUT_DIR, "problems")
    SIZES = [5, 10, 15, 20, 25] 
    REQUIRED_SUCCESSES = 5  # We want exactly this many solved instances per size
    RANDOM_SEED = 42
    
    # Planners to compare
    PLANNERS = ['pyperplan', 'fast-downward']

    os.makedirs(PROBLEMS_DIR, exist_ok=True)
    random.seed(RANDOM_SEED)

    results = []
    
    print(f"Starting Experiments... (Seed: {RANDOM_SEED})")
    print(f"Target: {REQUIRED_SUCCESSES} SOLVED instances per Grid Size.")
    print("-" * 100)
    print(f"{'Size':<5} | {'Run':<3} | {'Algo':<25} | {'Status':<10} | {'Time (s)':<8} | {'Nodes/Len':<10}")
    print("-" * 100)

    for N in SIZES:
        success_count = 0
        attempt_counter = 0 # To track how many maps we generated to find good ones

        while success_count < REQUIRED_SUCCESSES:
            attempt_counter += 1
            
            # 1. Generate Random Instance
            obstacles = []
            for r in range(N):
                for c in range(N):
                    if random.random() < 0.2:
                        obstacles.append((r, c))
            
            start, goal = (0, 0), (N - 1, N - 1)
            if start in obstacles:
                obstacles.remove(start)
            if goal in obstacles:
                obstacles.remove(goal)
            
            problem = GridProblem(N, start, goal, obstacles)

            # 2. Check Solvability (Filter) using A* Manhattan
            # We run this first. If it fails, we discard the map and retry.
            tracemalloc.start()
            t_start = time.time()
            path_manhattan, nodes_manhattan, gen, max_mem_nodes, avg_bf, max_bf, min_bf = a_star_search(problem, manhattan_distance)
            t_end = time.time()
            current, peak = tracemalloc.get_traced_memory()
            mem_manhattan = peak / 10**6
            tracemalloc.stop()

            if path_manhattan is None:
                # Map is unsolvable. Skip and retry.
                # Optional: print(f"  [Debug] Map {attempt_counter} unsolvable. Retrying...")
                continue
            
            # --- IF WE ARE HERE, THE MAP IS SOLVABLE ---
            run_id = success_count  # This is the 0..4 index of successful runs
            
            # A. Record A* Manhattan (since we already ran it)
            print(f"{N:<5} | {run_id:<3} | {'A* (Manhattan)':<25} | {'[SUCCESS]':<10} | {t_end - t_start:<8.4f} | {nodes_manhattan:<10}")
            results.append({
                'Size': N, 'Run': run_id, 'Algorithm': 'A* (Manhattan)',
                'Success': True, 'Time': t_end - t_start, 
                'Metric_Value': nodes_manhattan,
                'Nodes_Generated': gen,
                'Max_Mem_Nodes': max_mem_nodes,
                'Memory_MB': mem_manhattan,
                'Avg_Branching': avg_bf,
                'Max_Branching': max_bf,
                'Min_Branching': min_bf
            })

            # Visualize first run
            if run_id == 0:
                draw_grid(problem, path_manhattan, "A*", os.path.join(OUTPUT_DIR, f"vis_astar_{N}.png"))

            # B. Run A* Euclidean
            tracemalloc.start()
            t_start = time.time()
            path_euc, nodes_euc, gen_euc, max_mem_nodes_euc, avg_bf_euc, max_bf_euc, min_bf_euc = a_star_search(problem, euclidean_distance)
            t_end = time.time()
            current, peak = tracemalloc.get_traced_memory()
            mem_euc = peak / 10**6
            tracemalloc.stop()

            print(f"{N:<5} | {run_id:<3} | {'A* (Euclidean)':<25} | {'[SUCCESS]':<10} | {t_end - t_start:<8.4f} | {nodes_euc:<10}")
            results.append({
                'Size': N, 'Run': run_id, 'Algorithm': 'A* (Euclidean)',
                'Success': True, 'Time': t_end - t_start, 
                'Metric_Value': nodes_euc,
                'Nodes_Generated': gen_euc,
                'Max_Mem_Nodes': max_mem_nodes_euc,
                'Memory_MB': mem_euc,
                'Avg_Branching': avg_bf_euc,
                'Max_Branching': max_bf_euc,
                'Min_Branching': min_bf_euc
            })

            # C. Run Planners
            domain_file = "domain.pddl"
            prob_file_path = os.path.join(PROBLEMS_DIR, f"prob_{N}_{run_id}.pddl")
            generate_pddl_problem(problem, prob_file_path)

            for planner_name in PLANNERS:
                full_algo_name = f"Planner ({planner_name})"
                
                tracemalloc.start()
                start_time = time.time()
                
                plan = None
                try:
                    plan = run_planning_solver(domain_file, prob_file_path, planner_name)
                except Exception as e:
                    pass 

                end_time = time.time()
                current, peak = tracemalloc.get_traced_memory()
                mem_mb = peak / 10**6
                tracemalloc.stop()

                elapsed = end_time - start_time
                # Even if A* solved it, Planner might fail (timeout/crash), so we check 'plan'
                success_p = True if plan else False
                plan_len = len(plan) if plan else 0

                print(f"{N:<5} | {run_id:<3} | {full_algo_name:<25} | {'[SUCCESS]' if success_p else '[FAIL]':<10} | {elapsed:<8.4f} | {plan_len:<10}")

                results.append({
                    'Size': N, 'Run': run_id, 'Algorithm': full_algo_name,
                    'Success': success_p, 'Time': elapsed,
                    'Metric_Value': plan_len,
                    'Nodes_Generated': 0,
                    'Max_Mem_Nodes': 0,
                    'Memory_MB': mem_mb,
                    'Avg_Branching': 0,
                    'Max_Branching': 0,
                    'Min_Branching': 0
                })

                if run_id == 0 and success_p and planner_name == 'pyperplan':
                    draw_grid(problem, plan, "Planner", os.path.join(OUTPUT_DIR, f"vis_plan_{N}.png"))
            
            # Increment success counter only after finishing all algos for this map
            success_count += 1
            
        # Optional: Print how many attempts it took to find 5 valid maps
        print(f"  > Size {N}: Found {REQUIRED_SUCCESSES} solvable instances (Required {attempt_counter} generated maps).")

    # Save to CSV
    csv_path = os.path.join(OUTPUT_DIR, 'experiment_results.csv')
    with open(csv_path, 'w', newline='') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\nExperiments completed. Results saved to '{csv_path}'.")

if __name__ == "__main__":
    run_experiments()
