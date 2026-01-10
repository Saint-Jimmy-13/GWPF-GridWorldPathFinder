import heapq

class GridProblem:
    def __init__(self, size, start, goal, obstacles):
        """
        size: integer N for an N x N grid
        start: tuple (r, c)
        goal: tuple (r, c)
        obstacles: list of tuples [(r, c), ...] representing walls
        """
        self.size = size
        self.start = start
        self.goal = goal
        self.obstacles = set(obstacles) # Use a set for O(1) lookups
    
    def actions(self, state):
        """Returns valid moves from the current state (r, c)."""
        r, c = state
        candidates = [
            ('UP', (r - 1, c)),
            ('DOWN', (r + 1, c)),
            ('LEFT', (r, c - 1)),
            ('RIGHT', (r, c + 1))
        ]

        valid_moves = []
        for action_name, (nr, nc) in candidates:
            # Check bounds and obstacles
            if 0 <= nr < self.size and 0 <= nc < self.size:
                if (nr, nc) not in self.obstacles:
                    valid_moves.append((action_name, (nr, nc)))
        return valid_moves
    
    def step_cost(self, state, action, next_state):
        return 1    # Uniform cost for grid movement
    
    def goal_test(self, state):
        return state == self.goal

class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h
        
    # This defines how the Priority Queue compares nodes (by f-score)
    def __lt__(self, other):
        return self.f < other.f

def a_star_search(problem, heuristic_func):
    """
    A* Implementation
    Constraint: Duplicate elimination and NO reopening.
    Returns: (path_list, expanded_nodes_count)
    """
    # 1. Initialize
    start_node = Node(state=problem.start, g=0, h=heuristic_func(problem.start, problem.goal))

    # The frontier is a Priority Queue
    frontier = []
    heapq.heappush(frontier, start_node)

    # We need a way to check if a state is in the frontier and what its g-cost is
    # maps state -> node
    frontier_states = {start_node.state: start_node}
    explored = set()
    nodes_expanded = 0

    while frontier:
        # 2. Pop
        current_node = heapq.heappop(frontier)

        # In 'lazy' heap implementations, we might pop a node that was effectively "removed"
        # (replaced by a better one). We check if this is the current best version.
        if current_node.state in frontier_states and frontier_states[current_node.state] != current_node:
            continue    # Skip this "stale" node

        # Clean up frontier_states since it's leaving the frontier
        if current_node.state in frontier_states:
            del frontier_states[current_node.state]
        
        # 3. Goal Test (immediately after pop)
        if problem.goal_test(current_node.state):
            return reconstruct_path(current_node), nodes_expanded
        
        # 4. Add to explored
        explored.add(current_node.state)
        nodes_expanded += 1

        # 5. Expand
        for action_name, next_state in problem.actions(current_node.state):
            # NO REOPENING: If in explored, ignore completely.
            if next_state in explored:
                continue

            child_g = current_node.g + problem.step_cost(current_node.state, action_name, next_state)
            child_h = heuristic_func(next_state, problem.goal)
            child_node = Node(next_state, current_node, action_name, child_g, child_h)

            # If not in frontier: Insert
            if next_state not in frontier_states:
                heapq.heappush(frontier, child_node)
                frontier_states[next_state] = child_node
            
            # If in frontier with higher cost: Replace
            elif child_g < frontier_states[next_state].g:
                # To "replace" in a heap, we simply push the better node
                # and update our tracker. The old node becomes "stale"
                # and will be skipped when popped.
                heapq.heappush(frontier, child_node)
                frontier_states[next_state] = child_node

    return None, nodes_expanded  # Failure

def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    return path[::-1]   # Reverse to get Start -> Goal
