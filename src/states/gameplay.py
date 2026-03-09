import pygame
from states.base_state import BaseState
from utils.math_helpers import get_cell_from_mouse
from settings import (
    GRID_SIZE, CELL_SIZE, MARGIN,
    PLAYER_OFFSET, ENEMY_OFFSET,
    WHITE, BLACK, BLUE, RED, GRAY, GREEN, BG_COLOR,
    SCREEN_WIDTH,
)


class GameplayState(BaseState):

    def enter(self):
        snapshot = self.engine.pending_game_snapshot
        self.engine.pending_game_snapshot = None
        self.enemy_move_scheduled = False
        self.enemy_move_time = 0

        if snapshot and self.engine.load_game_snapshot(snapshot):
            return
            
        if not self.engine.game or self.engine.game_over_winner:
            self.engine.new_game()

    def handle_events(self, events):
        game = self.engine.game
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.engine.state_manager.push("pause")
                return
            if event.type == pygame.MOUSEBUTTONDOWN and game.turn == "player" and not self.enemy_move_scheduled:
                cell = get_cell_from_mouse(event.pos, ENEMY_OFFSET)
                if cell:
                    result = game.enemy.receive_attack(cell)
                    if result != "repeat":
                        if not game.enemy.all_sunk():
                            game.turn = "computer"
                            self.enemy_move_scheduled = True
                            self.enemy_move_time = pygame.time.get_ticks() + 800  # 0.8s delay
                        if not game.player.all_sunk() and not self.enemy_move_scheduled:
                            game.turn = "player"

    def update(self):
        game = self.engine.game
        
        if self.enemy_move_scheduled:
            if pygame.time.get_ticks() >= self.enemy_move_time:
                game.enemy_move()
                self.enemy_move_scheduled = False
                game.turn = "player"

        if game.enemy.all_sunk():
            self.engine.state_manager.change("game_over")
            self.engine.game_over_winner = "player"
        elif game.player.all_sunk():
            self.engine.state_manager.change("game_over")
            self.engine.game_over_winner = "computer"

    def draw(self, screen):
        game = self.engine.game
        screen.fill(BG_COLOR)
        self._draw_board(screen, game.player, PLAYER_OFFSET, show_ships=True)
        self._draw_board(screen, game.enemy, ENEMY_OFFSET, show_ships=False)
        self._draw_labels(screen)

    # -- helpers ----------------------------------------------------------

    @staticmethod
    def _draw_board(screen, board, offset_x, show_ships):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = offset_x + c * CELL_SIZE
                y = MARGIN + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if show_ships:
                    for ship in board.ships:
                        if (r, c) in ship.cells:
                            pygame.draw.rect(screen, GRAY, rect)

                if (r, c) in board.attacks:
                    hit = any((r, c) in ship.cells for ship in board.ships)
                    if hit:
                        pygame.draw.circle(screen, RED, rect.center, 10)
                    else:
                        pygame.draw.circle(screen, BLUE, rect.center, 8)

    @staticmethod
    def _draw_labels(screen):
        font = pygame.font.SysFont(None, 28)
        screen.blit(font.render("PLAYER", True, WHITE), (PLAYER_OFFSET, 10))
        screen.blit(font.render("ENEMY",  True, WHITE), (ENEMY_OFFSET, 10))
        hint = pygame.font.SysFont(None, 22).render("ESC — Pause", True, GRAY)
        screen.blit(hint, (SCREEN_WIDTH - hint.get_width() - MARGIN, 14))