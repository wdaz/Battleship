class DragController:
    def __init__(self):
        self.selected_ship = None
        self.is_dragging = False
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        self.start_row = None
        self.start_col = None
        self.start_orientation = None

    def start_drag(self, ship, offset_x, offset_y):
        self.selected_ship = ship
        self.is_dragging = True
        self.mouse_offset_x = offset_x
        self.mouse_offset_y = offset_y
        
        # Save original position in case drag is cancelled/invalid
        self.start_row = ship.row
        self.start_col = ship.col
        self.start_orientation = ship.orientation

        # Pick it up from the board to avoid self-collision checks
        ship.row = None
        ship.col = None

    def stop_drag(self):
        ship = self.selected_ship
        self.selected_ship = None
        self.is_dragging = False
        return ship

    def rotate_ship(self):
        if self.selected_ship:
            self.selected_ship.rotate()

    def revert_drag(self):
        if self.selected_ship:
            self.selected_ship.row = self.start_row
            self.selected_ship.col = self.start_col
            self.selected_ship.orientation = self.start_orientation
            self.stop_drag()
