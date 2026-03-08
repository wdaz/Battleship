from settings import GRID_SIZE, CELL_SIZE, MARGIN


def get_cell_from_mouse(pos, offset):
    """Convert a mouse pixel position to a board (row, col) or None."""
    x, y = pos
    if not (offset <= x <= offset + GRID_SIZE * CELL_SIZE):
        return None
    col = (x - offset) // CELL_SIZE
    row = (y - MARGIN) // CELL_SIZE
    if 0 <= row < GRID_SIZE:
        return (row, col)
    return None