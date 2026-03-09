from settings import GRID_SIZE

class PlacementShip:
    def __init__(self, length):
        self.length = length
        self.orientation = "H"
        self.row = None
        self.col = None
    
    def get_cells(self):
        if self.row is None or self.col is None:
            return []
        if self.orientation == "H":
            return [(self.row, self.col + i) for i in range(self.length)]
        else:
            return [(self.row + i, self.col) for i in range(self.length)]
    
    def rotate(self):
        self.orientation = "V" if self.orientation == "H" else "H"
        # Validate borders
        if self.row is not None and self.col is not None:
            if self.orientation == "H" and self.col + self.length > GRID_SIZE:
                self.col = GRID_SIZE - self.length
            if self.orientation == "V" and self.row + self.length > GRID_SIZE:
                self.row = GRID_SIZE - self.length

class ShipDock:
    def __init__(self):
        self.ships = []
        self._init_dock()

    def _init_dock(self):
        # length: count
        # 4 of len 1, 3 of len 2, 2 of len 3, 1 of len 4
        config = {1: 4, 2: 3, 3: 2, 4: 1}
        for length, count in config.items():
            for _ in range(count):
                self.ships.append(PlacementShip(length))
                
    def get_unplaced_ships(self):
        return [s for s in self.ships if s.row is None or s.col is None]

    def get_placed_ships(self):
        return [s for s in self.ships if s.row is not None and s.col is not None]
        
    def reset(self):
        for s in self.ships:
            s.row = None
            s.col = None
            s.orientation = "H"
