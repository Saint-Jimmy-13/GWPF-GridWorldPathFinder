import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_experiments(csv_file='output/experiment_results.csv', output_dir='output'):
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Run experiments.py first.")
        return

    df = pd.read_csv(csv_file)
    
    # Filter only Successful runs for Time/Memory analysis
    df_success = df[df['Success'] == True]
    
    # Group by Size and Algo
    df_avg = df_success.groupby(['Size', 'Algorithm']).mean().reset_index()
    
    # 1. Success Rate Calculation (using original DF)
    success_counts = df.groupby(['Size', 'Algorithm'])['Success'].mean().reset_index()
    success_pivot = success_counts.pivot(index='Size', columns='Algorithm', values='Success')

    # --- Plot 1: Success Rate ---
    plt.figure(figsize=(10, 6))
    success_pivot.plot(kind='bar', ax=plt.gca())
    plt.title('Success Rate by Grid Size')
    plt.ylabel('Success Rate (0.0 - 1.0)')
    plt.xlabel('Grid Size (N)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'plot_success_rate.png'))
    print(f"Generated {os.path.join(output_dir, 'plot_success_rate.png')}")
    plt.close()

    # --- Plot 2: Time (Only Successful Runs) ---
    plt.figure(figsize=(10, 6))
    time_pivot = df_avg.pivot(index='Size', columns='Algorithm', values='Time')
    for algo in time_pivot.columns:
        plt.plot(time_pivot.index, time_pivot[algo], marker='o', label=algo)
    
    plt.title('Avg Execution Time (Successful Runs Only)')
    plt.ylabel('Time (s)')
    plt.xlabel('Grid Size (N)')
    plt.legend()
    plt.grid(True, linestyle='--')
    plt.savefig(os.path.join(output_dir, 'plot_time.png'))
    print(f"Generated {os.path.join(output_dir, 'plot_time.png')}")
    plt.close()

    # --- Plot 3: A* Nodes Expanded ---
    nodes_df = df_avg[df_avg['Algorithm'] == 'A*']
    plt.figure(figsize=(10, 6))
    plt.plot(nodes_df['Size'], nodes_df['Metric_Value'], marker='^', color='green', label='A* Nodes')
    plt.title('Search Effort: A* Nodes Expanded')
    plt.ylabel('Count')
    plt.xlabel('Grid Size (N)')
    plt.legend()
    plt.grid(True, linestyle='--')
    plt.savefig(os.path.join(output_dir, 'plot_astar_nodes.png'))
    print(f"Generated {os.path.join(output_dir, 'plot_astar_nodes.png')}")
    plt.close()

if __name__ == "__main__":
    plot_experiments()
