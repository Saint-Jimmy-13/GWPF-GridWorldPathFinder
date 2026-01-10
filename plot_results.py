import pandas as pd
import matplotlib.pyplot as plt

def plot_experiments(csv_file='experiment_results.csv'):
    # 1. Load Data
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'. Run experiments.py first.")
        return
    
    # 2. Aggregate Data (Take the mean of the multiple runs for each size)
    # Grouped by 'Size' and 'Algorithm' to get the average Time, Memory, etc.
    df_avg = df.groupby(['Size', 'Algorithm']).mean().reset_index()

    # Pivot tables make it easier to plot lines for each algorithm
    # Index = Size, Columns = Algorithm, Values = Metric
    time_pivot = df_avg.pivot(index='Size', columns='Algorithm', values='Time')
    mem_pivot = df_avg.pivot(index='Size', columns='Algorithm', values='Memory_MB')

    # For "Nodes/Metric", we usually only care about A* Nodes Expanded for the report
    # beacuse Planner "Plan Length" is not directly comparable to "Nodes Expanded".
    nodes_df = df_avg[df_avg['Algorithm'] == 'A*']

    # --- Plot 1: Running Time Comparison ---
    plt.figure(figsize=(10, 6))
    for algo in time_pivot.columns:
        plt.plot(time_pivot.index, time_pivot[algo], marker='o', label=algo)

    plt.title('Execution Time: A* vs Planner', fontsize=14)
    plt.xlabel('Grid Size (NxN)', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('plot_time.png')
    print("Generated 'plot_time.png'")

    # --- Plot 2: Memory Usage Comparison ---
    plt.figure(figsize=(10, 6))
    for algo in mem_pivot.columns:
        plt.plot(mem_pivot.index, mem_pivot[algo], marker='s', linestyle='--', label=algo)
    
    plt.title('Memory Usage: A* vs Planner', fontsize=14)
    plt.xlabel('Grid Size (NxN)', fontsize=12)
    plt.ylabel('Peak Memory (MB)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('plot_memory.png')
    print("Generated 'plot_memory.png'")

    # --- Plot 3: A* Expanded Nodes (Scale Analysis) ---
    plt.figure(figsize=(10, 6))
    plt.plot(nodes_df['Size'], nodes_df['Metric_Value'], marker='^', color='green', label='A* Nodes')
    
    plt.title('Search Effort: A* Nodes Expanded', fontsize=14)
    plt.xlabel('Grid Size (NxN)', fontsize=12)
    plt.ylabel('Number of Nodes', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('plot_astar_nodes.png')
    print("Generated 'plot_astar_nodes.png'")

    # Optional: Show plots if running locally
    plt.show()

if __name__ == "__main__":
    plot_experiments()
