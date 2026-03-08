import random
from entities.ship import Ship
from settings import GRID_SIZE

SHIP_CONFIG = {
    1: 4,
    2: 3,
    3: 2,
    4: 1
}


class Board:
    def __init__(self):
        self.ships = []
        self.attacks = set()

    def occupied_cells(self):
        cells = set()
        for ship in self.ships:
            for c in ship.cells:
                cells.add(c)
        return cells

    def is_valid_position(self, cells):
        occ = self.occupied_cells()
        for r, c in cells:
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                return False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr = r + dr
                    nc = c + dc
                    if (nr, nc) in occ:
                        return False
        return True

    def place_ship(self, length):
        while True:
            orientation = random.choice(["H", "V"])
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)
            cells = []
            for i in range(length):
                r = row + (i if orientation == "V" else 0)
                c = col + (i if orientation == "H" else 0)
                cells.append((r, c))
            if self.is_valid_position(cells):
                self.ships.append(Ship(cells))
                return

    def place_all_ships(self):
        for length, count in SHIP_CONFIG.items():
            for _ in range(count):
                self.place_ship(length)

    def receive_attack(self, cell):
        if cell in self.attacks:
            return "repeat"
        self.attacks.add(cell)
        for ship in self.ships:
            if cell in ship.cells:
                ship.hit(cell)
                if ship.sunk():
                    return "sunk"
                return "hit"
        return "miss"

    def all_sunk(self):
        return all(ship.sunk() for ship in self.ships)
