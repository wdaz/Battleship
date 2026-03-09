import pygame
from states.base_state import BaseState
from utils.ui import Button, TextInput
from core import database
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BG_COLOR, DIFF_EASY, DIFF_MEDIUM, DIFF_HARD

_SECTION_COLOR = (140, 175, 210)
_HINT_OK       = ( 80, 200, 100)
_HINT_BAD      = (220,  90,  90)
_DIVIDER       = ( 65,  65,  85)
_NO_USERS_COL  = (105, 105, 128)
_OVERLAY       = (0, 0, 0, 150)
_MODAL_BG      = (42, 45, 72)
_MODAL_BORDER  = (95, 120, 160)


class MainMenuState(BaseState):

    def __init__(self, engine):
        super().__init__(engine)
        self._font_title   = pygame.font.SysFont(None, 80)
        self._font_section = pygame.font.SysFont(None, 30)
        self._font_label   = pygame.font.SysFont(None, 23)
        self._font_input   = pygame.font.SysFont(None, 30)
        self._font_btn     = pygame.font.SysFont(None, 26)

        self._text_input = None
        self._start_btn  = None
        self._user_btns  = []
        self._modal_user = None
        self._modal_rect = None
        self._continue_btn = None
        self._new_game_btn = None

        self._modal_mode = None
        self._modal_mode_rect = None
        self._mode_static_btn = None
        self._mode_dynamic_btn = None

        self._modal_diff_rect = None
        self._diff_easy_btn = None
        self._diff_med_btn = None
        self._diff_hard_btn = None

    # ------------------------------------------------------------------
    def enter(self):
        database.init_db()
        users = database.get_recent_users(10)

        # ── New-player section (left half, centred at x = SCREEN_WIDTH // 4) ──
        left_cx = SCREEN_WIDTH // 4          # 255 for a 1020-wide screen
        in_w, in_h = 300, 44
        in_x = left_cx - in_w // 2
        in_y = 158

        self._text_input = TextInput(
            rect=(in_x, in_y, in_w, in_h),
            font=self._font_input,
            max_length=30,
            placeholder="Enter your name…",
        )
        self._text_input.focused = True       # auto-focus on entry

        btn_w, btn_h = 160, 44
        self._start_btn = Button(
            rect=(left_cx - btn_w // 2, in_y + in_h + 22, btn_w, btn_h),
            text="START",
            font=self._font_btn,
            enabled=False,
            on_click=self._on_start_click,
        )

        # ── Existing-user buttons (right half, centred at x = SCREEN_WIDTH * 3 // 4) ──
        right_cx = SCREEN_WIDTH * 3 // 4     # 765 for a 1020-wide screen
        ubtn_w, ubtn_h = 340, 36
        ubtn_x = right_cx - ubtn_w // 2

        self._user_btns = []
        for i, name in enumerate(users):
            self._user_btns.append(
                Button(
                    rect=(ubtn_x, 150 + i * 43, ubtn_w, ubtn_h),
                    text=name,
                    font=self._font_btn,
                    enabled=True,
                    on_click=lambda n=name: self._on_user_click(n),
                )
            )

        self._modal_user = None
        self._modal_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 230,
            SCREEN_HEIGHT // 2 - 115,
            460,
            230,
        )
        btn_w, btn_h = 300, 42
        btn_x = self._modal_rect.centerx - btn_w // 2
        first_btn_y = self._modal_rect.y + 108
        second_btn_y = first_btn_y + btn_h + 12
        self._continue_btn = Button(
            rect=(btn_x, first_btn_y, btn_w, btn_h),
            text="Continue Last Game",
            font=self._font_btn,
            on_click=self._on_continue_choice,
        )
        self._new_game_btn = Button(
            rect=(btn_x, second_btn_y, btn_w, btn_h),
            text="Start New Game",
            font=self._font_btn,
            on_click=self._on_new_game_choice,
        )

        # Modals rects
        self._modal_mode_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)
        self._modal_diff_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 130, 400, 260)
        
        md_btn_w, md_btn_h = 240, 40
        md_btn_x = self._modal_mode_rect.centerx - md_btn_w // 2
        self._mode_static_btn = Button(
            rect=(md_btn_x, self._modal_mode_rect.y + 70, md_btn_w, md_btn_h),
            text="Static Difficulty", font=self._font_btn, on_click=self._on_static_choice
        )
        self._mode_dynamic_btn = Button(
            rect=(md_btn_x, self._modal_mode_rect.y + 70 + md_btn_h + 10, md_btn_w, md_btn_h),
            text="Dynamic Difficulty", font=self._font_btn, on_click=self._on_dynamic_choice
        )

        df_btn_w, df_btn_h = 240, 40
        df_btn_x = self._modal_diff_rect.centerx - df_btn_w // 2
        dy = self._modal_diff_rect.y + 70
        self._diff_easy_btn = Button(
            rect=(df_btn_x, dy, df_btn_w, df_btn_h),
            text="EASY", font=self._font_btn, on_click=lambda: self._start_game_with_diff(DIFF_EASY)
        )
        self._diff_med_btn = Button(
            rect=(df_btn_x, dy + df_btn_h + 10, df_btn_w, df_btn_h),
            text="MEDIUM", font=self._font_btn, on_click=lambda: self._start_game_with_diff(DIFF_MEDIUM)
        )
        self._diff_hard_btn = Button(
            rect=(df_btn_x, dy + 2*(df_btn_h + 10), df_btn_w, df_btn_h),
            text="HARD", font=self._font_btn, on_click=lambda: self._start_game_with_diff(DIFF_HARD)
        )

    # ------------------------------------------------------------------
    def _on_start_click(self) -> None:
        name = self._text_input.value.strip()
        if 3 <= len(name) <= 30:
            database.upsert_user(name)
            self._modal_user = name
            self._modal_mode = "mode_choice"

    def _on_user_click(self, name: str) -> None:
        self._modal_user = name
        if database.has_game_state(name):
            self._modal_mode = "save_choice"
        else:
            self._modal_mode = "mode_choice"

    def _on_continue_choice(self) -> None:
        if not self._modal_user:
            return
        self._login(self._modal_user, continue_saved=True, difficulty=DIFF_EASY)

    def _on_new_game_choice(self) -> None:
        self._modal_mode = "mode_choice"

    def _on_static_choice(self) -> None:
        self._modal_mode = "diff_choice"

    def _on_dynamic_choice(self) -> None:
        if not self._modal_user: return
        rating = database.get_user_rating(self._modal_user)
        if rating < 0:
            diff = DIFF_EASY
        elif rating > 0:
            diff = DIFF_HARD
        else:
            diff = DIFF_MEDIUM
        self._start_game_with_diff(diff)

    def _start_game_with_diff(self, diff: str) -> None:
        if not self._modal_user: return
        self._login(self._modal_user, continue_saved=False, difficulty=diff)

    def _close_modal(self) -> None:
        self._modal_user = None
        self._modal_mode = None

    def _login(self, name: str, continue_saved: bool, difficulty: str) -> None:
        database.upsert_user(name)
        self.engine.active_username = name
        self.engine.pending_game_snapshot = None

        if continue_saved:
            self.engine.pending_game_snapshot = database.load_game_state(name)
            self._close_modal()
            self.engine.state_manager.change("gameplay")
        else:
            database.delete_game_state(name)
            self._close_modal()
            # We want to create the game here with the chosen difficulty before going to placement
            self.engine.new_game(difficulty=difficulty)
            self.engine.state_manager.change("ship_placement")

    # ------------------------------------------------------------------
    def handle_events(self, events):
        if self._modal_user and self._modal_mode:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._close_modal()
                    return
                # route to correct buttons based on mode
                if self._modal_mode == "save_choice":
                    self._continue_btn.handle_event(event)
                    self._new_game_btn.handle_event(event)
                elif self._modal_mode == "mode_choice":
                    self._mode_static_btn.handle_event(event)
                    self._mode_dynamic_btn.handle_event(event)
                elif self._modal_mode == "diff_choice":
                    self._diff_easy_btn.handle_event(event)
                    self._diff_med_btn.handle_event(event)
                    self._diff_hard_btn.handle_event(event)
            return

        for event in events:
            self._text_input.handle_event(event)
            self._start_btn.handle_event(event)
            for btn in self._user_btns:
                btn.handle_event(event)

            # Enter key shortcut while input is focused
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
                and self._text_input.focused
            ):
                self._on_start_click()

    def update(self):
        self._text_input.update()
        stripped = self._text_input.value.strip()
        self._start_btn.enabled = 3 <= len(stripped) <= 30

    def draw(self, screen):
        screen.fill(BG_COLOR)

        # ── Title ──────────────────────────────────────────────────────
        title = self._font_title.render("BATTLESHIP", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # ── Horizontal divider ─────────────────────────────────────────
        pygame.draw.line(screen, _DIVIDER, (40, 110), (SCREEN_WIDTH - 40, 110), 1)

        # ── Vertical divider between panels ───────────────────────────
        mid = SCREEN_WIDTH // 2
        pygame.draw.line(screen, _DIVIDER, (mid, 118), (mid, SCREEN_HEIGHT - 20), 1)

        # ── Left panel label ───────────────────────────────────────────
        left_cx = SCREEN_WIDTH // 4
        lbl_new = self._font_section.render("New Player", True, _SECTION_COLOR)
        screen.blit(lbl_new, (left_cx - lbl_new.get_width() // 2, 120))

        # ── Text input ─────────────────────────────────────────────────
        self._text_input.draw(screen)

        # ── Character hint ─────────────────────────────────────────────
        raw      = self._text_input.value
        stripped = raw.strip()
        n        = len(stripped)
        if raw:
            if n < 3:
                hint_text  = f"{n}/30 — minimum 3 characters"
                hint_color = _HINT_BAD
            else:
                hint_text  = f"{n}/30"
                hint_color = _HINT_OK
            hint = self._font_label.render(hint_text, True, hint_color)
            screen.blit(hint, (
                self._text_input.rect.x,
                self._text_input.rect.bottom + 5,
            ))

        # ── Start button ───────────────────────────────────────────────
        self._start_btn.draw(screen)

        # ── Right panel ────────────────────────────────────────────────
        right_cx = SCREEN_WIDTH * 3 // 4
        if self._user_btns:
            lbl_p = self._font_section.render("Players", True, _SECTION_COLOR)
            screen.blit(lbl_p, (right_cx - lbl_p.get_width() // 2, 120))
            for btn in self._user_btns:
                btn.draw(screen)
        else:
            msg = self._font_label.render(
                "No saved players yet — type your name on the left.",
                True, _NO_USERS_COL,
            )
            screen.blit(msg, (right_cx - msg.get_width() // 2, 300))

        if self._modal_user and self._modal_mode:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(_OVERLAY)
            screen.blit(overlay, (0, 0))

            if self._modal_mode == "save_choice":
                r = self._modal_rect
                pygame.draw.rect(screen, _MODAL_BG, r, border_radius=10)
                pygame.draw.rect(screen, _MODAL_BORDER, r, 2, border_radius=10)

                title = self._font_section.render(self._modal_user, True, WHITE)
                message = self._font_label.render("Continue your last game or start a new one?", True, WHITE)
                screen.blit(title, (r.centerx - title.get_width() // 2, r.y + 26))
                screen.blit(message, (r.centerx - message.get_width() // 2, r.y + 64))

                self._continue_btn.draw(screen)
                self._new_game_btn.draw(screen)

            elif self._modal_mode == "mode_choice":
                r = self._modal_mode_rect
                pygame.draw.rect(screen, _MODAL_BG, r, border_radius=10)
                pygame.draw.rect(screen, _MODAL_BORDER, r, 2, border_radius=10)
                
                title = self._font_section.render("Difficulty Mode", True, WHITE)
                message = self._font_label.render("Choose how difficulty is determined", True, WHITE)
                screen.blit(title, (r.centerx - title.get_width() // 2, r.y + 15))
                screen.blit(message, (r.centerx - message.get_width() // 2, r.y + 45))

                self._mode_static_btn.draw(screen)
                self._mode_dynamic_btn.draw(screen)

            elif self._modal_mode == "diff_choice":
                r = self._modal_diff_rect
                pygame.draw.rect(screen, _MODAL_BG, r, border_radius=10)
                pygame.draw.rect(screen, _MODAL_BORDER, r, 2, border_radius=10)

                title = self._font_section.render("Static Difficulty", True, WHITE)
                screen.blit(title, (r.centerx - title.get_width() // 2, r.y + 20))

                self._diff_easy_btn.draw(screen)
                self._diff_med_btn.draw(screen)
                self._diff_hard_btn.draw(screen)