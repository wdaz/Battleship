import pygame
from states.base_state import BaseState
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, GREEN, RED, BG_COLOR


class GameOverState(BaseState):

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.engine.state_manager.change("gameplay")

    def draw(self, screen):
        # Let gameplay draw the final board underneath
        gameplay = self.engine.state_manager._states.get("gameplay")
        if gameplay:
            gameplay.draw(screen)

        font = pygame.font.SysFont(None, 28)
        winner = getattr(self.engine, "game_over_winner", None)
        y_base = SCREEN_HEIGHT - 65

        if winner == "player":
            text = font.render("PLAYER WINS", True, GREEN)
        else:
            text = font.render("COMPUTER WINS", True, RED)

        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_base))
        restart = font.render("Press R to Restart", True, WHITE)
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, y_base + 30))