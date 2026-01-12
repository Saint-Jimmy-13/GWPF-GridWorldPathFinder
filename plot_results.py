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
    df_avg = df_success.groupby(['Size', 'Algorithm']).mean(numeric_only=True).reset_index()

    # Generic helper to save plots
    def save_plot(pivot_data, title, ylabel, filename, log_scale=False):
        plt.figure(figsize=(10, 6))
        for column in pivot_data.columns:
            plt.plot(pivot_data.index, pivot_data[column], marker='o', label=column)
        
        if log_scale:
            plt.yscale('log')
            ylabel += " (Log Scale)"
            
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel('Grid Size (N)')
        plt.legend()
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.savefig(os.path.join(output_dir, filename))
        plt.close()

    # --- Plot 1: Execution Time (Log Scale) ---
    pivot_time = df_avg.pivot(index='Size', columns='Algorithm', values='Time')
    save_plot(pivot_time, 'Execution Time', 'Time (s)', 'plot_time.png', log_scale=True)

    # --- Plot 2: A* Nodes Expanded vs Generated ---
    # We only look at A* for node metrics
    astar_df = df_avg[df_avg['Algorithm'].str.contains("A*")]
    
    # Expanded
    pivot_expanded = astar_df.pivot(index='Size', columns='Algorithm', values='Metric_Value')
    save_plot(pivot_expanded, 'A* Search Effort: Nodes Expanded', 'Nodes Expanded', 'plot_astar_expanded.png')

    # Generated
    pivot_generated = astar_df.pivot(index='Size', columns='Algorithm', values='Nodes_Generated')
    save_plot(pivot_generated, 'A* Search Effort: Nodes Generated', 'Nodes Generated', 'plot_astar_generated.png')

    # --- Plot 3: Memory Usage (Abstract Nodes) ---
    # "Maximum number of nodes kept in memory"
    pivot_mem_nodes = astar_df.pivot(index='Size', columns='Algorithm', values='Max_Mem_Nodes')
    save_plot(pivot_mem_nodes, 'Max Nodes in Memory (Frontier + Explored)', 'Node Count', 'plot_memory_nodes.png')

    # --- Plot 4: Physical Memory (MB) ---
    pivot_mem_mb = df_avg.pivot(index='Size', columns='Algorithm', values='Memory_MB')
    save_plot(pivot_mem_mb, 'Physical Memory Usage', 'Peak Memory (MB)', 'plot_memory_mb.png')

    # --- Plot 5: Branching Factor ---
    pivot_bf = astar_df.pivot(index='Size', columns='Algorithm', values='Avg_Branching')
    save_plot(pivot_bf, 'Average Effective Branching Factor', 'Branching Factor', 'plot_branching.png')

    print(f"Plots generated in '{output_dir}/' folder.")

if __name__ == "__main__":
    plot_experiments()
