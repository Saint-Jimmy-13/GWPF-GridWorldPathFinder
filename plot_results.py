import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_experiments(csv_file='output/experiment_results.csv', output_dir='output'):
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found.")
        return

    df = pd.read_csv(csv_file)
    
    # Filter Successful runs for performance metrics
    df_success = df[df['Success'] == True]
    df_avg = df_success.groupby(['Size', 'Algorithm']).mean().reset_index()

    # --- Plot 1: Execution Time (Log Scale) ---
    plt.figure(figsize=(10, 6))
    pivot_time = df_avg.pivot(index='Size', columns='Algorithm', values='Time')
    
    for column in pivot_time.columns:
        plt.plot(pivot_time.index, pivot_time[column], marker='o', label=column)
        
    plt.yscale('log')   # Log scale is crucial here!
    plt.title('Execution Time (Log Scale)')
    plt.ylabel('Time (seconds) - Log Scale')
    plt.xlabel('Grid Size (N)')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.savefig(os.path.join(output_dir, 'plot_time.png'))
    plt.close()

    # --- Plot 2: A* Search Effort (Nodes Expanded) ---
    # Filter only A* algorithms
    astar_df = df_avg[df_avg['Algorithm'].str.contains("A*")]
    pivot_nodes = astar_df.pivot(index='Size', columns='Algorithm', values='Metric_Value')

    plt.figure(figsize=(10, 6))
    for column in pivot_nodes.columns:
        plt.plot(pivot_nodes.index, pivot_nodes[column], marker='^', label=column)
        
    plt.title('Heuristic Comparison: Nodes Expanded')
    plt.ylabel('Nodes Expanded')
    plt.xlabel('Grid Size (N)')
    plt.legend()
    plt.grid(True, ls="--")
    plt.savefig(os.path.join(output_dir, 'plot_astar_nodes.png'))
    plt.close()

    print("Plots generated in 'output/' folder.")

if __name__ == "__main__":
    plot_experiments()
