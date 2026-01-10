import time
import random
import csv
import tracemalloc  # For memory measurement
from grid_problem import GridProblem, a_star_search
from planning_utils import generate_pddl_problem, run_planning_solver
from visualizer import draw_grid

# Heuristic for A* (Manhattan Distance)
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def run_experiments():
    # Define scaling parameters (Grid Sizes)
    sizes = [5, 10, 15, 20, 25]
    num_runs_per_size = 5   # Run multiple time to get an average

    results = []

    print(f"{'Size':<6} | {'Algo':<10} | {'Time (s)':<10} | {'Nodes/Plan Len':<15} | {'Memory (MB)':<10} | {'Avg BF':<10} | {'Max BF':<10}")
    print("-" * 65)

    for N in sizes:
        for run_i in range(num_runs_per_size):
            # --- 1. Generate Random Instance ---
            # Random obstacles (approx 20% coverage)
            obstacles = []
            for r in range(N):
                for c in range(N):
                    if random.random() < 0.2:
                        obstacles.append((r, c))
            
            # Ensure start/goal are unique and not obstacles
            start = (0, 0)
            goal = (N - 1, N - 1)
            if start in obstacles:
                obstacles.remove(start)
            if goal in obstacles:
                obstacles.remove(goal)
            
            problem = GridProblem(N, start, goal, obstacles)

            # --- 2. Run A* ---
            tracemalloc.start()
            start_time = time.time()

            path_a_star, node_count, avg_bf, max_bf = a_star_search(problem, manhattan_distance)

            end_time = time.time()
            a_star_mem = tracemalloc.get_traced_memory()[1] / 10**6 # Convert to MB
            tracemalloc.stop()

            a_star_time = end_time - start_time

            # Save A* Visualization for the first run of each size
            if run_i == 0 and path_a_star:
                draw_grid(problem, path_a_star, "A*", f"vis_astar_{N}.png")

            results.append({
                'Size': N,
                'Run': run_i,
                'Algorithm': 'A*',
                'Time': a_star_time,
                'Metric_Value': node_count, # Nodes expanded
                'Memory_MB': a_star_mem,
                'Avg_Branching': avg_bf,
                'Max_Branching': max_bf
            })

            print(f"{N:<6} | {'A*':<10} | {a_star_time:<10.4f} | {node_count:<15} | {a_star_mem:<10.4f} | AvgBF: {avg_bf:10.2f} MaxBF: {max_bf:<10}")

            # --- 3. Run Planner ---
            # Generate PDDL files
            domain_file = "domain.pddl"
            # Ensure domain.pddl exists in directory
            problem_file = generate_pddl_problem(problem, f"problems/prob_{N}_{run_i}.pddl")

            tracemalloc.start()
            start_time = time.time()

            plan = run_planning_solver(domain_file, problem_file)

            end_time = time.time()
            planner_mem = tracemalloc.get_traced_memory()[1] / 10**6 # Convert to MB
            tracemalloc.stop()

            planner_time = end_time - start_time

            plan_length = len(plan) if plan else 0

            if run_i == 0 and plan:
                draw_grid(problem, plan, "Planner", f"vis_plan_{N}.png")

            results.append({
                'Size': N,
                'Run': run_i,
                'Algorithm': 'Planner',
                'Time': planner_time,
                'Metric_Value': plan_length,    # Plan length
                'Memory_MB': planner_mem
            })

            print(f"{N:<6} | {'Planner':<10} | {planner_time:<10.4f} | {plan_length:<15} | {planner_mem:<10.4f}")

    # --- 4. Save to CSV ---
    keys = results[0].keys()
    with open('experiment_results.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    
    print("\nExperiments completed. Results saved to 'experiment_results.csv'.")

if __name__ == "__main__":
    run_experiments()
