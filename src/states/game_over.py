import pygame
from states.base_state import BaseState
from utils.ui import Button
from core import database
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, RED

_OVERLAY_COLOR = (0, 0, 0, 160)
_PANEL_BG      = (42, 45, 72)
_PANEL_BORDER  = (80, 100, 140)

class GameOverState(BaseState):

    _BTN_W       = 220
    _BTN_H       = 44
    _BTN_GAP     = 14
    _PAD_H       = 70
    _PAD_TOP     = 90
    _PAD_BOT     = 32

    def __init__(self, engine):
        super().__init__(engine)
        self._font_title = pygame.font.SysFont(None, 48)
        self._font_btn   = pygame.font.SysFont(None, 28)
        self._buttons    = []

        n = 2
        panel_w = self._BTN_W + 2 * self._PAD_H
        panel_h = (self._PAD_TOP
                   + n * self._BTN_H
                   + (n - 1) * self._BTN_GAP
                   + self._PAD_BOT)

        self._panel_rect = pygame.Rect(
            SCREEN_WIDTH  // 2 - panel_w // 2,
            SCREEN_HEIGHT // 2 - panel_h // 2,
            panel_w, panel_h,
        )
        self.winner = None

    def enter(self):
        self.selected_index = 0
        self.winner = getattr(self.engine, "game_over_winner", None)
        
        username = self.engine.active_username
        if username:
            database.delete_game_state(username)
            if self.winner == "player":
                database.update_user_rating(username, 1)
            elif self.winner == "computer":
                database.update_user_rating(username, -1)

        btn_x = self._panel_rect.centerx - self._BTN_W // 2
        btn_y_start = self._panel_rect.y + self._PAD_TOP

        labels_and_actions = [
            ("New Game", self._new_game),
            ("Main Menu", self._main_menu),
        ]

        self._buttons = [
            Button(
                rect=(btn_x,
                      btn_y_start + i * (self._BTN_H + self._BTN_GAP),
                      self._BTN_W, self._BTN_H),
                text=label,
                font=self._font_btn,
                on_click=action,
            )
            for i, (label, action) in enumerate(labels_and_actions)
        ]

    def _new_game(self):
        diff = getattr(self.engine, "selected_difficulty", "Easy")
        if getattr(self.engine, "game", None):
            diff = getattr(self.engine.game, "difficulty", diff)
        
        self.engine.new_game(difficulty=diff)
        self.engine.state_manager.change("ship_placement")

    def _main_menu(self):
        self.engine.state_manager.change("main_menu")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self._buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self._buttons)
                elif event.key == pygame.K_RETURN:
                    if self._buttons[self.selected_index].on_click:
                        self._buttons[self.selected_index].on_click()
                    return

            if event.type == pygame.MOUSEMOTION:
                for i, btn in enumerate(self._buttons):
                    if btn.rect.collidepoint(event.pos):
                        self.selected_index = i

            for btn in self._buttons:
                btn.handle_event(event)

        for i, btn in enumerate(self._buttons):
            btn._hovered = (i == self.selected_index)

    def draw(self, screen):
        gameplay = self.engine.state_manager._states.get("gameplay")
        if gameplay:
            gameplay.draw(screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(_OVERLAY_COLOR)
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, _PANEL_BG,     self._panel_rect, border_radius=12)
        pygame.draw.rect(screen, _PANEL_BORDER, self._panel_rect, 2, border_radius=12)

        title_str = "PLAYER WINS" if self.winner == "player" else "COMPUTER WINS"
        title_color = GREEN if self.winner == "player" else RED

        title = self._font_title.render(title_str, True, title_color)
        screen.blit(
            title,
            (SCREEN_WIDTH // 2 - title.get_width() // 2, self._panel_rect.y + 20),
        )

        for btn in self._buttons:
            btn.draw(screen)
