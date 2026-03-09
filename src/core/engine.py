import pygame
from entities.board import Board
from entities.ai import RandomAI, HuntTargetAI, ProbabilityAI
from entities.ship import Ship
from core.state_manager import StateManager
from core.events import EventManager
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, DIFF_EASY, DIFF_MEDIUM, DIFF_HARD


def _get_ai_from_diff(diff: str):
    if diff == DIFF_HARD:
        return ProbabilityAI()
    elif diff == DIFF_MEDIUM:
        return HuntTargetAI()
    else:
        return RandomAI()

class Game:
    """Pure game-logic container (no rendering)."""

    def __init__(self, difficulty=DIFF_EASY):
        self.player = Board()
        self.enemy = Board()
        self.player.place_all_ships()
        self.enemy.place_all_ships()
        self.turn = "player"
        self.difficulty = difficulty
        self.ai = _get_ai_from_diff(difficulty)

    def enemy_move(self):
        cell = self.ai.choose_attack(self.player)
        return self.player.receive_attack(cell)


class Engine:
    """Main application class — owns the pygame window and game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battleship")
        self.clock = pygame.time.Clock()
        self.running = False

        self.event_manager = EventManager()
        self.state_manager = StateManager()
        self.game = None
        self.game_over_winner = None
        self.active_username = None
        self.pending_game_snapshot = None

        self._register_states()

    def _register_states(self):
        from states.main_menu import MainMenuState
        from states.gameplay import GameplayState
        from states.game_over import GameOverState
        from states.pause import PauseState
        from states.ship_placement import ShipPlacementState

        self.state_manager.register("main_menu", MainMenuState(self))
        self.state_manager.register("ship_placement", ShipPlacementState(self))
        self.state_manager.register("gameplay",  GameplayState(self))
        self.state_manager.register("game_over", GameOverState(self))
        self.state_manager.register("pause",     PauseState(self))

    def new_game(self, difficulty=DIFF_EASY):
        self.game = Game(difficulty=difficulty)
        self.game_over_winner = None

    @staticmethod
    def _board_to_dict(board: Board) -> dict:
        return {
            "ships": [
                {
                    "cells": [[r, c] for r, c in ship.cells],
                    "hits": [[r, c] for r, c in ship.hits],
                }
                for ship in board.ships
            ],
            "attacks": [[r, c] for r, c in board.attacks],
        }

    @staticmethod
    def _board_from_dict(payload: dict) -> Board:
        board = Board()
        board.ships = []
        board.attacks = set()

        for item in payload.get("ships", []):
            cells = [tuple(cell) for cell in item.get("cells", [])]
            ship = Ship(cells)
            ship.hits = {tuple(cell) for cell in item.get("hits", [])}
            board.ships.append(ship)

        board.attacks = {tuple(cell) for cell in payload.get("attacks", [])}
        return board

    def game_to_snapshot(self) -> dict | None:
        if self.game is None:
            return None
        return {
            "player": self._board_to_dict(self.game.player),
            "enemy": self._board_to_dict(self.game.enemy),
            "turn": self.game.turn,
            "difficulty": self.game.difficulty,
        }

    def load_game_snapshot(self, snapshot: dict) -> bool:
        try:
            game = Game.__new__(Game)
            game.player = self._board_from_dict(snapshot["player"])
            game.enemy = self._board_from_dict(snapshot["enemy"])
            game.turn = snapshot.get("turn", "player")
            if game.turn not in {"player", "computer"}:
                game.turn = "player"
            game.difficulty = snapshot.get("difficulty", DIFF_EASY)
            game.ai = _get_ai_from_diff(game.difficulty)
        except (KeyError, TypeError, ValueError):
            return False

        self.game = game
        self.game_over_winner = None
        return True

    def run(self):
        self.running = True
        self.state_manager.change("main_menu")

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state_manager.handle_events(events)
            self.state_manager.update()
            self.state_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()