import random
from entities.ai.base_ai import BaseAI
from settings import GRID_SIZE

class HuntTargetAI(BaseAI):
    """
    Medium difficulty AI:
    - Hunt phase: randomly shoots in a checkerboard pattern.
    - Target phase: shoots adjacent cells upon hit.
    """
    def __init__(self):
        self.mode = "hunt"
        self.target_hits = []    # (r, c)
        self.potential_targets = []  # (r, c)
        self.hunt_parity = random.choice([0, 1])

    def choose_attack(self, board):
        self._update_state(board)

        if self.mode == "target" and self.potential_targets:
            choice = self.potential_targets.pop()
            return choice
        else:
            # Hunt mode
            return self._hunt(board.attacks)

    def _update_state(self, board):
        # Examine board hits to find any non-sunk hit ships
        # This prevents AI from forgetting state across restarts or states.
        all_hits = set()
        for ship in board.ships:
            if not ship.sunk():
                all_hits.update(ship.hits)
        
        # If we have unsunk hits, we should be in target mode
        if all_hits:
            self.mode = "target"
            self.target_hits = list(all_hits)
            
            # Recalculate potential targets
            self.potential_targets = []
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for hit in self.target_hits:
                r, c = hit
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        if (nr, nc) not in board.attacks and (nr, nc) not in self.potential_targets:
                            self.potential_targets.append((nr, nc))
                            
            # Sort potential targets (maybe prioritize lines if we have 2+ hits)
            if len(self.target_hits) > 1:
                self._prioritize_linear_targets()
                
        else:
            self.mode = "hunt"
            self.target_hits = []
            self.potential_targets = []

    def _prioritize_linear_targets(self):
        # Extra optimization to guess directions based on multiple hits
        pass
        
    def _hunt(self, attacks):
        valid_cells = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) not in attacks and (r + c) % 2 == self.hunt_parity:
                    valid_cells.append((r, c))
                    
        if not valid_cells:
            # Fallback if no checkerboard pattern cells remain
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    if (r, c) not in attacks:
                        valid_cells.append((r, c))
                        
        return random.choice(valid_cells)