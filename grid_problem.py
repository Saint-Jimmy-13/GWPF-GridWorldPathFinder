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
    
    def result(self, state, action):
        """Return the new state after applying the action."""
        # In our simple grid, the action tuple already contains the new coordinate
        # Example action: ('UP', (0, 1)) -> returns (0, 1)
        return action[1]
    
    def goal_test(self, state):
        return state == self.goal
    
    def step_cost(self, state, action, next_state):
        return 1    # Uniform cost for grid movement
