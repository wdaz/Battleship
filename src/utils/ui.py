"""Reusable Pygame UI widgets: Button and TextInput."""

import pygame

# ── Colour palette ────────────────────────────────────────────────────────────
_BTN_NORMAL    = (60,  120, 170)
_BTN_HOVER     = (90,  155, 205)
_BTN_DISABLED  = (65,   65,  78)
_BTN_TEXT      = (255, 255, 255)
_BTN_TEXT_DIS  = (120, 120, 130)
_BTN_BORDER    = (180, 200, 225)

_IN_BG          = (38,  38,  50)
_IN_BORDER      = (100, 149, 237)
_IN_BORDER_FOCUS= (255, 225,  70)
_IN_TEXT        = (255, 255, 255)
_IN_PLACEHOLDER = (105, 105, 128)
_CURSOR_COLOR   = (255, 255, 255)


class Button:
    """Clickable button with hover and disabled visual states."""

    def __init__(self, rect, text: str, font, enabled: bool = True, on_click=None):
        self.rect      = pygame.Rect(rect)
        self.text      = text
        self.font      = font
        self.enabled   = enabled
        self.on_click  = on_click
        self._hovered  = False

    # ------------------------------------------------------------------
    def handle_event(self, event) -> bool:
        """Pass a pygame event; returns True if the button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self.rect.collidepoint(event.pos)

        if (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            if self.on_click:
                self.on_click()
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        if not self.enabled:
            bg = _BTN_DISABLED
        elif self._hovered:
            bg = _BTN_HOVER
        else:
            bg = _BTN_NORMAL

        pygame.draw.rect(surface, bg,          self.rect, border_radius=6)
        pygame.draw.rect(surface, _BTN_BORDER, self.rect, 1, border_radius=6)

        text_col  = _BTN_TEXT if self.enabled else _BTN_TEXT_DIS
        text_surf = self.font.render(self.text, True, text_col)

        # Clip text so it never spills outside the button boundary
        pad      = 8
        clip     = pygame.Rect(
            self.rect.x + pad, self.rect.y + 2,
            self.rect.width - 2 * pad, self.rect.height - 4,
        )
        old_clip = surface.get_clip()
        surface.set_clip(clip)
        surface.blit(
            text_surf,
            (
                self.rect.centerx - text_surf.get_width()  // 2,
                self.rect.centery - text_surf.get_height() // 2,
            ),
        )
        surface.set_clip(old_clip)


class TextInput:
    """Single-line text input field with a blinking cursor and length cap."""

    def __init__(self, rect, font, max_length: int = 30, placeholder: str = ""):
        self.rect        = pygame.Rect(rect)
        self.font        = font
        self.max_length  = max_length
        self.placeholder = placeholder
        self.value       = ""
        self.focused     = False
        self._cursor_vis  = True
        self._cursor_tick = pygame.time.get_ticks()

    # ------------------------------------------------------------------
    def handle_event(self, event) -> None:
        """Pass a pygame event to update focus state and value."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.focused = self.rect.collidepoint(event.pos)

        if not self.focused:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif (
                event.unicode
                and event.unicode.isprintable()
                and len(self.value) < self.max_length
            ):
                self.value += event.unicode

    def update(self) -> None:
        """Advance cursor blink animation; call once per frame."""
        if not self.focused:
            self._cursor_vis  = False
            self._cursor_tick = pygame.time.get_ticks()
            return
        now = pygame.time.get_ticks()
        if now - self._cursor_tick >= 530:
            self._cursor_vis  = not self._cursor_vis
            self._cursor_tick = now

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, _IN_BG,    self.rect, border_radius=6)
        border = _IN_BORDER_FOCUS if self.focused else _IN_BORDER
        pygame.draw.rect(surface, border,    self.rect, 2, border_radius=6)

        pad = 10
        if self.value:
            text_surf = self.font.render(self.value, True, _IN_TEXT)
        else:
            text_surf = self.font.render(self.placeholder, True, _IN_PLACEHOLDER)

        clip = pygame.Rect(
            self.rect.x + pad, self.rect.y + 2,
            self.rect.width - 2 * pad, self.rect.height - 4,
        )
        old_clip = surface.get_clip()
        surface.set_clip(clip)
        ty = self.rect.centery - text_surf.get_height() // 2
        surface.blit(text_surf, (self.rect.x + pad, ty))
        surface.set_clip(old_clip)

        # Blinking cursor (drawn after restoring clip so it isn't cut off)
        if self.focused and self._cursor_vis:
            value_w = self.font.size(self.value)[0] if self.value else 0
            cx = self.rect.x + pad + value_w + 1
            cx = min(cx, self.rect.right - pad - 3)   # clamp inside box
            pygame.draw.line(
                surface, _CURSOR_COLOR,
                (cx, self.rect.y  + 7),
                (cx, self.rect.bottom - 7),
                2,
            )
