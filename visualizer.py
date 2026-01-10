"""
Visualization module for grid pathfinding solutions.
Renders grids with obstacles, paths, and solution details.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re
from pathlib import Path

def draw_grid(problem, path=None, algorithm_name="Solution", output_file=None):
    """
    Visualizes the grid, obstacles, and the path found by an algorithm.
    
    Args:
        problem: GridProblem instance
        path: List of actions (strings) or coordinates (tuples).
              - For A*: ['UP', 'DOWN', 'LEFT', 'RIGHT', ...]
              - For Planner: ['move(cell_0_0, cell_0_1)', ...]
        algorithm_name: Name of algorithm ('A*', 'Planner', etc.) for the title
        output_file: If provided, save visualization to this file.
                     If None, display interactively.
    """

    fig, ax = plt.subplots(figsize=(8, 8))

    # 1. Setup Grid
    N = problem.size
    ax.set_xlim(-0.5, N - 0.5)
    ax.set_ylim(N - 0.5, 0.5)   # Flip Y so (0, 0) is top-left
    ax.set_aspect('equal')
    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.grid(True, color='gray', alpha=0.3, linewidth=0.5)

    # 2. Draw Obstacles (Black squares)
    for r, c in problem.obstacles:
        rect = patches.Rectangle(
            (c - 0.5, r - 0.5), 1, 1,
            linewidth=1,
            edgecolor='black',
            facecolor='black',
            alpha=0.8
        )
        ax.add_patch(rect)
    
    # 3. Draw Start (Green) and Goal (Red)
    sr, sc = problem.start
    gr, gc = problem.goal

    # Start position
    rect_start = patches.Rectangle(
        (sc - 0.5, sr - 0.5), 1, 1,
        linewidth=2,
        edgecolor='darkgreen',
        facecolor='lightgreen',
        alpha=0.7
    )
    ax.add_patch(rect_start)
    ax.text(sc, sr, 'S', ha='center', va='center', fontweight='bold', fontsize=12)

    # Goal position
    rect_goal = patches.Rectangle(
        (gc - 0.5, gr - 0.5), 1, 1,
        linewidth=2,
        edgecolor='darkred',
        facecolor='salmon',
        alpha=0.7
    )
    ax.add_patch(rect_goal)
    ax.text(gc, gr, 'G', ha='center', va='center', fontweight='bold', fontsize=12)

    # 4. Draw Path (Blue line with markers)
    if path:
        try:
            path_coords = parse_path(problem, path, algorithm_name)

            if path_coords and len(path_coords) > 0:
                # Extract coordinates for plotting (center of cells)
                ys = [r for r, c in path_coords]
                xs = [c for r, c in path_coords]

                # Draw path as blue line
                ax.plot(xs, ys, color='dodgerblue', linewidth=2.5, alpha=0.8,
                        marker='o', markersize=4, markerfacecolor='blue', markeredgecolor='darkblue')
                
                # Hihghlight intermediate waypoints
                if len(path_coords) > 2:
                    for r, c in path_coords[1:-1]:
                        circle = patches.Circle((c, r), 0.15, color='blue', alpha=0.5)
                        ax.add_patch(circle)
        except Exception as e:
            print(f"Warning: Could not parse path: {e}")
    
    # 5. Title and labels
    path_len = len(path) if path else 0
    title = f"{algorithm_name} Solution"
    if path_len > 0:
        title += f" (Path Length: {path_len})"
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Column", fontsize=11)
    ax.set_ylabel("Row", fontsize=11)
    
    # Add grid size annotation
    ax.text(0.98, 0.02, f"Grid: {N}x{N}", transform=ax.transAxes,
            fontsize=10, ha='right', va='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Save or show
    if output_file:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"  Saved visualization: {output_file}")
        plt.close()
    else:
        plt.tight_layout()
        plt.show()

def parse_path(problem, path, algo):
    """
    Converts a list of action strings into a list of (r, c) coordinates.
    
    Handles two formats:
    - A* format: ['UP', 'DOWN', 'LEFT', 'RIGHT', ...]
    - PDDL Planner format: ['move(cell_0_0, cell_0_1)', 'move(cell_0_1, cell_1_1)', ...]
    
    Args:
        problem: GridProblem instance
        path: List of action strings
        algo: Algorithm name ('A*' or 'Planner') to determine format
        
    Returns:
        list: List of (r, c) coordinate tuples representing the path
    """

    coords = [problem.start]
    curr_r, curr_c = problem.start

    if algo == 'A*' or algo.startswith('A*'):
        # A* returns direction actions: ['DOWN', 'RIGHT', ...], etc.
        moves = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        for action in path:
            action_upper = action.upper()
            dr, dc = moves.get(action_upper, (0, 0))
            curr_r += dr
            curr_c += dc

            # Verify new position is valid
            if 0 <= curr_r < problem.size and 0 <= curr_c < problem.size:
                coords.append((curr_r, curr_c))
            else:
                print(f"Warning: Invalid move {action} to ({curr_r}, {curr_c})")
                break
    
    elif algo == 'Planner' or 'PDDL' in algo:
        # PDDL Planner returns actions like: 'move(cell_0_0, cell_0_1)'
        # We extract the destination cell from each move string

        for action_str in path:
            # Regex to find coordinates: cell_r_c
            # Match the last occurrence (destination) in the action
            matches = re.findall(r'cell_(\d+)_(\d+)', str(action_str))

            if matches and len(matches) >= 2:
                # Use the second match (destination)
                r, c = int(matches[-1][0]), int(matches[-1][1])

                # Verify the move is valid (adjacent cells)
                if abs(r - curr_r) + abs(c - curr_c) == 1:
                    coords.append((r, c))
                    curr_r, curr_c = r, c
                else:
                    print(f"Warning: Non-adjacent move in action: {action_str}")
            elif matches and len(matches) == 1:
                # Single match - might be source or dest
                r, c = int(matches[0][0]), int(matches[0][1])
                if abs(r - curr_r) + abs(c - curr_c) == 1:
                    coords.append((r, c))
                    curr_r, curr_c = r, c
    
    return coords
