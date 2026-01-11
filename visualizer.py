import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re
import os

def draw_grid(problem, path=None, algorithm_name="Solution", output_file=None):
    """
    Visualizes the grid, obstacles, and the path found.
    path: List of actions (strings).
    algorithm_name: 'A*' or 'Planner' (affects how we parse the path).
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    # 1. Setup Grid
    N = problem.size
    ax.set_xlim(0, N)
    ax.set_ylim(N, 0)   # Flip Y so (0, 0) is top-left
    ax.set_aspect('equal')
    ax.set_xticks(range(N + 1))
    ax.set_yticks(range(N + 1))
    ax.grid(True, color='black', alpha=0.2)

    # 2. Draw Obstacles (Black squares)
    for r, c in problem.obstacles:
        # matplotlib patches use (x, y) which corrsponds to (col, row)
        rect = patches.Rectangle((c, r), 1, 1, linewidth=0, facecolor='black')
        ax.add_patch(rect)
    
    # 3. Draw Start (Green) and Goal (Red)
    sr, sc = problem.start
    gr, gc = problem.goal

    # Start
    rect_start = patches.Rectangle((sc, sr), 1, 1, linewidth=0, facecolor='lime', alpha=0.6)
    ax.add_patch(rect_start)
    ax.text(sc + 0.5, sr + 0.5, 'S', ha='center', va='center', fontweight='bold')

    # Goal
    rect_goal = patches.Rectangle((gc, gr), 1, 1, linewidth=0, facecolor='red', alpha=0.6)
    ax.add_patch(rect_goal)
    ax.text(gc + 0.5, gr + 0.5, 'G', ha='center', va='center', fontweight='bold')

    # 4. Draw Path (Blue line)
    if path:
        path_coords = parse_path(problem, path, algorithm_name)

        # Extract X (col) and Y (row) for plotting
        ys = [r + 0.5 for r, c in path_coords]  # Center of cell
        xs = [c + 0.5 for r, c in path_coords]

        ax.plot(xs, ys, color='blue', linewidth=3, alpha=0.7, marker='o', markersize=5)
    
    plt.title(f"{algorithm_name} Solution (Len: {len(path) if path else 0})")

    if output_file:
        # Ensure dir exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        plt.savefig(output_file)
        print(f"  -> Saved visualization: {output_file}")
    else:
        plt.show()
    plt.close()

def parse_path(problem, path, algo):
    """
    Converts a list of action strings into a list of (r, c) coordinates.
    """
    coords = [problem.start]
    curr_r, curr_c = problem.start

    if algo == 'A*':
        # A* returns directions: ['DOWN', 'RIGHT', ...]
        moves = {
            'UP': (-1, 0), 'DOWN': (1, 0),
            'LEFT': (0, -1), 'RIGHT': (0, 1)
        }
        for action in path:
            dr, dc = moves.get(action, (0, 0))
            curr_r += dr
            curr_c += dc
            coords.append((curr_r, curr_c))
    
    elif algo == 'Planner':
        # Planner returns PDDL: ['move(cell_0_0, cell_0_1)', ...]
        # We extract the destination cell from each move string
        for action_str in path:
            # Regex to find the second cell (destination)
            # Looks for: any_text(cell_r_c, cell_dest_r_dest_c)
            match = re.search(r'cell_(\d+)_(\d+)\)$', action_str)
            if match:
                r, c = int(match.group(1)), int(match.group(2))
                coords.append((r, c))
    
    return coords
