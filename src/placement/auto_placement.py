import random
from settings import GRID_SIZE
from placement.placement_validator import PlacementValidator

class AutoPlacement:
    @staticmethod
    def arrange(ship_dock):
        ship_dock.reset()
        validator = PlacementValidator()
        
        for ship in ship_dock.ships:
            placed = False
            while not placed:
                orientation = random.choice(["H", "V"])
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - 1)
                
                # Preliminary bounds check
                if orientation == "H" and col + ship.length > GRID_SIZE:
                    continue
                if orientation == "V" and row + ship.length > GRID_SIZE:
                    continue
                
                if validator.is_valid(row, col, ship.length, orientation, ship_dock.get_placed_ships()):
                    ship.orientation = orientation
                    ship.row = row
                    ship.col = col
                    placed = True
