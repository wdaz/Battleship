import random
from entities.ai.base_ai import BaseAI
from settings import GRID_SIZE

class RandomAI(BaseAI):
    """Easy difficulty AI: picks random cells that have not been attacked."""
    def choose_attack(self, board):
        while True:
            r = random.randint(0, GRID_SIZE - 1)
            c = random.randint(0, GRID_SIZE - 1)
            if (r, c) not in board.attacks:
                return r, c
