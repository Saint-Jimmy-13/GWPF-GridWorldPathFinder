import heapq
from typing import List, Tuple, Set, Optional, Callable, Dict

# Type aliases for clarity
State = Tuple[int, int]
Action = str

class GridProblem:
    def __init__(self, size: int, start: State, goal: State, obstacles: List[State]):
        """
        size: integer N for an N x N grid
        start: tuple (r, c)
        goal: tuple (r, c)
        obstacles: list of tuples [(r, c), ...] representing walls
        """
        self.size = size
        self.start = start
        self.goal = goal
        self.obstacles: Set[State] = set(obstacles) # Use a set for O(1) lookups
    
    def actions(self, state: State) -> List[Tuple[Action, State]]:
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
    
    def step_cost(self, state: State, action: Action, next_state: State) -> int:
        return 1    # Uniform cost for grid movement
    
    def goal_test(self, state: State) -> bool:
        return state == self.goal

class Node:
    def __init__(self, state: State, parent: Optional['Node'] = None, action: Optional[Action] = None, g: int = 0, h: int = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
        self.f = g + h
        
    # Priority Queue comparison by f-score
    def __lt__(self, other):
        return self.f < other.f
    
def reconstruct_path(node: Node) -> List[Action]:
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    return path[::-1]   # Reverse to get Start -> Goal

def a_star_search(problem: GridProblem, heuristic_func: Callable[[State, State], int]):
    """
    A* Implementation
    Constraint: Duplicate elimination and NO reopening.
    Returns: (path, nodes_expanded, avg_branching_factor, max_branching_factor)
    """
    # 1. Initialize
    start_h = heuristic_func(problem.start, problem.goal)
    start_node = Node(state=problem.start, g=0, h=start_h)

    # The frontier is a Priority Queue
    frontier = []
    heapq.heappush(frontier, start_node)

    # Frontier lookup map: state -> node
    frontier_states: Dict[State, Node] = {start_node.state: start_node}
    explored: Set[State] = set()
    
    # Stats Variables
    nodes_expanded = 0
    total_branching = 0
    max_branching = 0

    while frontier:
        # 2. Pop
        current_node = heapq.heappop(frontier)

        # Lazy Deletion Check: If we found a better path to this state previously,
        # the old "worse" node is still in the heap but removed from frontier_states.
        if current_node.state in frontier_states and frontier_states[current_node.state] != current_node:
            continue    # Skip stale node

        # Remove from frontier set
        if current_node.state in frontier_states:
            del frontier_states[current_node.state]
        
        # 3. Goal Test (immediately after pop)
        if problem.goal_test(current_node.state):
            avg_bf = total_branching / nodes_expanded if nodes_expanded > 0 else 0
            return reconstruct_path(current_node), nodes_expanded, avg_bf, max_branching
        
        # 4. Add to explored
        explored.add(current_node.state)
        nodes_expanded += 1

        # Count successors for this specific node
        current_successors = 0

        # 5. Expand
        for action_name, next_state in problem.actions(current_node.state):
            # NO REOPENING: If in explored, ignore completely.
            if next_state in explored:
                continue

            # This is a valid child generation
            current_successors += 1

            child_g = current_node.g + problem.step_cost(current_node.state, action_name, next_state)
            child_h = heuristic_func(next_state, problem.goal)
            child_node = Node(next_state, current_node, action_name, child_g, child_h)

            # Case A: Not in frontier -> Insert
            if next_state not in frontier_states:
                heapq.heappush(frontier, child_node)
                frontier_states[next_state] = child_node
            
            # Case B: In frontier with higher cost -> Replace
            elif child_g < frontier_states[next_state].g:
                # We push the new better node. The old one becomes "stale".
                heapq.heappush(frontier, child_node)
                frontier_states[next_state] = child_node
        
        # Update Stats
        total_branching += current_successors
        if current_successors > max_branching:
            max_branching = current_successors

    return None, nodes_expanded, 0, 0   # Failure
