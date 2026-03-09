from entities.board import Board
from entities.ship import Ship

class PlacementValidator:
    def __init__(self):
        self.temp_board = Board()
        
    def _sync_board(self, placed_ships, ignore_ship=None):
        self.temp_board.ships = []
        for s in placed_ships:
            if s is ignore_ship:
                continue
            cells = s.get_cells()
            if cells:
                self.temp_board.ships.append(Ship(cells))

    def is_valid(self, start_row, start_col, length, orientation, placed_ships, ignore_ship=None):
        self._sync_board(placed_ships, ignore_ship)
        
        # calculate cells
        if orientation == "H":
            cells = [(start_row, start_col + i) for i in range(length)]
        else:
            cells = [(start_row + i, start_col) for i in range(length)]
            
        return self.temp_board.is_valid_position(cells)
