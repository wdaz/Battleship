import random


class SimpleAI:
    def choose_move(self, board):
        while True:
            r = random.randint(0, 9)
            c = random.randint(0, 9)
            if (r, c) not in board.attacks:
                return (r, c)