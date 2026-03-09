from abc import ABC, abstractmethod


class BaseAI(ABC):
    @abstractmethod
    def choose_attack(self, board):
        """
        Takes the enemy's board and returns the (row, col) coordinate
        for the AI's next attack.
        """
        pass
