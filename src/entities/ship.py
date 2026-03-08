class Ship:
    def __init__(self, cells):
        self.cells = cells
        self.hits = set()

    def hit(self, cell):
        if cell in self.cells:
            self.hits.add(cell)

    def sunk(self):
        return len(self.hits) == len(self.cells)