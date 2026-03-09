import random
from entities.ai.base_ai import BaseAI
from settings import GRID_SIZE

class ProbabilityAI(BaseAI):
    """
    Hard difficulty AI:
    - Calculates a probability map of all possible ship placements
    - Skips placements that intersect known misses or sunk ships
    - Attacks the cell with the highest probability
    """
    def choose_attack(self, board):
        # Determine remaining ships
        remaining_ships_lengths = [len(ship.cells) for ship in board.ships if not ship.sunk()]
        
        # Determine known misses and hits
        hits = set()
        sunk_cells = set()
        for ship in board.ships:
            if ship.sunk():
                sunk_cells.update(ship.cells)
            else:
                hits.update(ship.hits)
                
        misses = set()
        for r, c in board.attacks:
            if (r, c) not in hits and (r, c) not in sunk_cells:
                misses.add((r, c))
                
        # Calculate probabilities
        prob_map = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        
        for length in remaining_ships_lengths:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    # Horizontal
                    if c + length <= GRID_SIZE:
                        cells = [(r, c + i) for i in range(length)]
                        self._add_to_prob_map(prob_map, cells, misses, sunk_cells, hits)
                    # Vertical
                    if r + length <= GRID_SIZE:
                        cells = [(r + i, c) for i in range(length)]
                        self._add_to_prob_map(prob_map, cells, misses, sunk_cells, hits)
                        
        # Find the maximum probability cell
        max_prob = -1
        best_cells = []
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) in board.attacks:
                    continue
                prob = prob_map[r][c]
                if prob > max_prob:
                    max_prob = prob
                    best_cells = [(r, c)]
                elif prob == max_prob:
                    best_cells.append((r, c))
                    
        if best_cells:
            return random.choice(best_cells)
            
        # Fallback
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if (r, c) not in board.attacks:
                    return r, c
                    
    def _add_to_prob_map(self, prob_map, cells, misses, sunk_cells, hits):
        # Invalid if it overlaps miss or sunk ship
        for cell in cells:
            if cell in misses or cell in sunk_cells:
                return
                
        # Boost probability significantly if placement overlaps known hits
        # (It means this ship configuration is very likely actual)
        overlap_hits = sum(1 for cell in cells if cell in hits)
        score = 1
        if overlap_hits > 0:
            score += 10 * overlap_hits
            
        for r, c in cells:
            prob_map[r][c] += score
