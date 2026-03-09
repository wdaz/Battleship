from placement.ship_dock import ShipDock
from placement.placement_validator import PlacementValidator
from placement.auto_placement import AutoPlacement
from placement.drag_controller import DragController

class PlacementSystem:
    def __init__(self):
        self.dock = ShipDock()
        self.validator = PlacementValidator()
        self.drag_controller = DragController()

    def auto_arrange(self):
        AutoPlacement.arrange(self.dock)

    def reset(self):
        self.dock.reset()

    def is_all_placed(self):
        return len(self.dock.get_unplaced_ships()) == 0
        
    def check_valid_placement(self, row, col, ship):
        return self.validator.is_valid(row, col, ship.length, ship.orientation, self.dock.get_placed_ships(), ignore_ship=ship)

    def attempt_drop(self, row, col):
        ship = self.drag_controller.selected_ship
        if not ship:
            return False
            
        # Basic bounds check just in case
        if ship.orientation == "H" and col + ship.length > 10: # GRID_SIZE
            self.drag_controller.revert_drag()
            return False
        if ship.orientation == "V" and row + ship.length > 10:
            self.drag_controller.revert_drag()
            return False

        if self.check_valid_placement(row, col, ship):
            ship.row = row
            ship.col = col
            self.drag_controller.stop_drag()
            return True
        else:
            self.drag_controller.revert_drag()
            return False

    def get_board_ships(self):
        # Converts PlacementShips to dicts or pure logic Ship structures?
        # The game engine might just need Board to place them.
        pass
