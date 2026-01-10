"""
Results plotting and analysis module.
Generates comparison charts from experiment results CSV.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_experiments(csv_file='experiment_results.csv', output_dir='plots'):
    """
    Generate comprehensive comparison plots from experiment results.
    
    Creates:
    - Running time comparison (A* vs Planner)
    - Memory usage comparison
    - A* nodes expanded (search effort)
    - Branching factor analysis
    - Solution quality (path length) comparison
    
    Args:
        csv_file: Path to results CSV file
        output_dir: Directory to save plot files
    """

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Load Data
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"ERROR: Could not find file '{csv_file}'")
        print("Please run experiments.py first to generate results.")
        return
    
    print("\n" + "="*80)
    print(f"Plotting results from {csv_file}")
    print("="*80 + "\n")
    
    # Aggregate data: take the mean across runs for each size and algorithm
    df_avg = df.groupby(['Size', 'Algorithm']).agg({
        'Time_s': 'mean',
        'Memory_MB': 'mean',
        'Nodes_Expanded': 'mean',
        'Plan_Length': 'mean',
        'Avg_Branching': 'mean',
        'Max_Branching': 'mean'
    }).reset_index()

    # Create pivot tables for easier plotting
    time_pivot = df_avg.pivot(index='Size', columns='Algorithm', values='Time_s')
    mem_pivot = df_avg.pivot(index='Size', columns='Algorithm', values='Memory_MB')
    nodes_pivot = df_avg.pivot(index='Size', columns='Algorithm', values='Nodes_Expanded')
    path_pivot = df_avg.pivot(index='Size', columns='Algorithm', values='Path_Length')

    # For A* heuristics, get the Manhattan results (most standard)
    df_astar = df[df['Algorithm'] == 'A*']
    df_astar_manhattan = df_astar[df_astar['Heuristic'] == 'Manhattan']
    df_astar_avg = df_astar_manhattan.groupby('Size').agg({
        'Time_s': 'mean',
        'Memory_MB': 'mean',
        'Nodes_Expanded': 'mean',
        'Avg_Branching': 'mean',
        'Max_Branching': 'mean',
        'Path_Length': 'mean'
    }).reset_index()

    # --- Plot 1: Running Time Comparison ---
    plt.figure(figsize=(12, 7))

    for algo in time_pivot.columns:
        plt.plot(time_pivot.index, time_pivot[algo], marker='o', linewidth=2.5,
                 markersize=8, label=algo, alpha=0.8)

    plt.title('Execution Time: A* vs PDDL Planning', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Grid Size (NxN)', fontsize=12, fontweight='bold')
    plt.ylabel('Time (seconds)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11, loc='upper left')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_execution_time.png', dpi=150, bbox_inches='tight')
    print("Generated: 01_execution_time.png")
    plt.close()

    # --- Plot 2: Memory Usage Comparison ---
    plt.figure(figsize=(12, 7))

    for algo in mem_pivot.columns:
        plt.plot(mem_pivot.index, mem_pivot[algo], marker='s', linewidth=2.5,
                 markersize=8, label=algo, linestyle='--', alpha=0.8)
    
    plt.title('Peak Memory Usage: A* vs PDDL Planning', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Grid Size (NxN)', fontsize=12, fontweight='bold')
    plt.ylabel('Peak Memory (MB)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11, loc='upper left')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_memory_usage.png', dpi=150, bbox_inches='tight')
    print("Generated: 02_memory_usage.png")
    plt.close()

    # --- Plot 3: A* Search Effort (Nodes Expanded) ---
    plt.figure(figsize=(12, 7))

    plt.plot(df_astar_avg['Size'], df_astar_avg['Nodes_Expanded'], marker='^',
             color='forestgreen', linewidth=2.5, markersize=9, label='A* Nodes Expanded', alpha=0.85)
    
    plt.title('A* Search Effort: Nodes Expanded vs Grid Size', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Grid Size (NxN)', fontsize=12, fontweight='bold')
    plt.ylabel('Number of Nodes Expanded', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_astar_nodes_expanded.png', dpi=150, bbox_inches='tight')
    print("Generated: 03_astar_nodes_expanded.png")
    plt.close()
    
    plt.title('Search Effort: A* Nodes Expanded', fontsize=14)
    plt.xlabel('Grid Size (NxN)', fontsize=12)
    plt.ylabel('Number of Nodes', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.savefig('plot_astar_nodes.png')
    print("Generated 'plot_astar_nodes.png'")

    # --- Plot 4: Branching Factor Analysis ---
    plt.figure(figsize=(12, 7))
    
    plt.plot(df_astar_avg['Size'], df_astar_avg['Avg_Branching'], marker='D',
             color='darkorange', linewidth=2.5, markersize=8, label='Avg Branching Factor',
             alpha=0.8)
    plt.plot(df_astar_avg['Size'], df_astar_avg['Max_Branching'], marker='D',
             color='red', linewidth=2.5, markersize=8, label='Max Branching Factor',
             linestyle='--', alpha=0.8)
    
    plt.title('A* Branching Factor Analysis', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Grid Size (NxN)', fontsize=12, fontweight='bold')
    plt.ylabel('Branching Factor', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11, loc='best')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_branching_factor.png', dpi=150, bbox_inches='tight')
    print("Generated: 04_branching_factor.png")
    plt.close()

    # --- Plot 5: Solution Quality (Path Length Comparison) ---
    plt.figure(figsize=(12, 7))
    
    for algo in path_pivot.columns:
        plt.plot(path_pivot.index, path_pivot[algo], marker='o', linewidth=2.5,
                 markersize=8, label=algo, alpha=0.8)
    
    plt.title('Solution Quality: Path Length Comparison', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Grid Size (NxN)', fontsize=12, fontweight='bold')
    plt.ylabel('Path Length (steps)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_path_length_comparison.png', dpi=150, bbox_inches='tight')
    print("Generated: 05_path_length_comparison.png")
    plt.close()

    # --- Plot 6: Time per Node (Efficiency Metric) ---
    plt.figure(figsize=(12, 7))
    
    # Time per node for A* (only where nodes > 0)
    df_astar_efficient = df_astar_avg[df_astar_avg['Nodes_Expanded'] > 0].copy()
    df_astar_efficient['Time_per_Node'] = (df_astar_efficient['Time_s'] / 
                                           df_astar_efficient['Nodes_Expanded'] * 1000) # ms
    
    plt.plot(df_astar_efficient['Size'], df_astar_efficient['Time_per_Node'],
             marker='o', color='purple', linewidth=2.5, markersize=8,
             label='A* Time per Node', alpha=0.85)
    
    plt.title('A* Efficiency: Time per Node Expanded', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Grid Size (NxN)', fontsize=12, fontweight='bold')
    plt.ylabel('Time per Node (milliseconds)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/06_time_per_node.png', dpi=150, bbox_inches='tight')
    print("Generated: 06_time_per_node.png")
    plt.close()

    # --- Summary Statistics ---
    print("\n" + "-"*80)
    print("SUMMARY STATISTICS")
    print("-"*80)
    
    print("\nAverage Results by Grid Size and Algorithm:")
    print(df_avg.to_string(index=False))
    
    print("\n" + "="*80)
    print(f"All plots saved to: {output_dir}/")
    print("="*80 + "\n")

if __name__ == "__main__":
    plot_experiments()
