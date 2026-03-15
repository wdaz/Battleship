import pygame
from states.base_state import BaseState
from settings import *
from utils.ui import Button
from placement.placement_system import PlacementSystem

class ShipPlacementState(BaseState):
    def __init__(self, engine):
        super().__init__(engine)
        self.sys = PlacementSystem()
        self._font_header = pygame.font.SysFont(None, 36)
        self._font_btn = pygame.font.SysFont(None, 24)
        
        btn_y = SCREEN_HEIGHT - MARGIN - 40
        btn_w = 180
        btn_h = 40
        btn_gap = 20
        
        start_x = SCREEN_WIDTH // 2 - (btn_w * 1.5 + btn_gap * 1)
        
        self.btn_auto = Button(
            (start_x, btn_y, btn_w, btn_h),
            "AUTO ARRANGE",
            self._font_btn,
            on_click=self.on_auto_arrange
        )
        
        self.btn_reset = Button(
            (start_x + btn_w + btn_gap, btn_y, btn_w, btn_h),
            "RESET",
            self._font_btn,
            on_click=self.on_reset
        )
        
        self.btn_start = Button(
            (start_x + (btn_w + btn_gap) * 2, btn_y, btn_w, btn_h),
            "START BATTLE",
            self._font_btn,
            on_click=self.on_start_battle
        )
        
        self.mouse_pos = (0, 0)
        
        # Dock dimensions
        self.dock_x = ENEMY_OFFSET
        self.dock_y = MARGIN
        self._init_dock_positions()

    def _init_dock_positions(self):
        # Assign fixed visual positions for ships in dock
        y_offset = self.dock_y
        for i, ship in enumerate(self.sys.dock.ships):
            ship.dock_x = self.dock_x + (i % 2) * 180
            ship.dock_y = y_offset + (i // 2) * 60

    def enter(self):
        # We start with empty board
        self.sys.reset()
        self.btn_start.enabled = False
        
    def exit(self):
        pass

    def on_auto_arrange(self):
        self.sys.auto_arrange()

    def on_reset(self):
        self.sys.reset()
        
    def on_start_battle(self):
        # Transfer placed ships back to Game Engine logic
        if self.sys.is_all_placed():
            from entities.ship import Ship
            self.engine.new_game()
            
            # Wipe enemy board (since it's auto-generated) and player board to manual
            self.engine.game.player.ships = []
            
            for s in self.sys.dock.get_placed_ships():
                cells = s.get_cells()
                self.engine.game.player.ships.append(Ship(cells))
                
            self.engine.state_manager.change("gameplay")

    def handle_events(self, events):
        for event in events:
            self.btn_auto.handle_event(event)
            self.btn_reset.handle_event(event)
            
            self.btn_start.enabled = self.sys.is_all_placed()
            if self.btn_start.enabled:
                self.btn_start.handle_event(event)
                
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    self._handle_pickup(event.pos)
                elif event.button == 3: # Right click
                    self.sys.drag_controller.rotate_ship()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.sys.drag_controller.is_dragging:
                        self._handle_drop(event.pos)
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.sys.drag_controller.rotate_ship()
                elif event.key == pygame.K_ESCAPE:
                    self.engine.state_manager.change("main_menu")

    def _handle_pickup(self, pos):
        # Check placed ships
        for ship in self.sys.dock.get_placed_ships():
            rect = self._get_ship_rect(ship)
            if rect.collidepoint(pos):
                self.sys.drag_controller.start_drag(ship, pos[0] - rect.x, pos[1] - rect.y)
                return
                
        # Check unplaced ships in dock
        for ship in self.sys.dock.get_unplaced_ships():
            rect = self._get_dock_rect(ship)
            if rect.collidepoint(pos):
                self.sys.drag_controller.start_drag(ship, pos[0] - rect.x, pos[1] - rect.y)
                return

    def _handle_drop(self, pos):
        # Convert dropped pixel to grid
        ship = self.sys.drag_controller.selected_ship
        x = pos[0] - self.sys.drag_controller.mouse_offset_x
        y = pos[1] - self.sys.drag_controller.mouse_offset_y
        
        # Grid bounds
        grid_rect = pygame.Rect(PLAYER_OFFSET, MARGIN, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        
        # Center of the first cell of the ship (to snap better)
        cell_center_x = x + CELL_SIZE // 2
        cell_center_y = y + CELL_SIZE // 2
        
        if grid_rect.collidepoint(cell_center_x, cell_center_y):
            col = (cell_center_x - PLAYER_OFFSET) // CELL_SIZE
            row = (cell_center_y - MARGIN) // CELL_SIZE
            
            # Auto-push boundaries if rotated near edge
            if ship.orientation == "H" and col + ship.length > GRID_SIZE:
                col = GRID_SIZE - ship.length
            if ship.orientation == "V" and row + ship.length > GRID_SIZE:
                row = GRID_SIZE - ship.length
                
            self.sys.attempt_drop(row, col)
        else:
            # Dropped outside grid
            self.sys.drag_controller.revert_drag()

    def _get_ship_rect(self, ship):
        if ship.row is None or ship.col is None:
            return self._get_dock_rect(ship)
        w = ship.length * CELL_SIZE if ship.orientation == "H" else CELL_SIZE
        h = CELL_SIZE if ship.orientation == "H" else ship.length * CELL_SIZE
        return pygame.Rect(PLAYER_OFFSET + ship.col * CELL_SIZE, MARGIN + ship.row * CELL_SIZE, w, h)

    def _get_dock_rect(self, ship):
        w = ship.length * CELL_SIZE if ship.orientation == "H" else CELL_SIZE
        h = CELL_SIZE if ship.orientation == "H" else ship.length * CELL_SIZE
        return pygame.Rect(getattr(ship, 'dock_x', 0), getattr(ship, 'dock_y', 0), w, h)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        self._draw_grid(screen, PLAYER_OFFSET, "PLAYER")
        
        # Draw hidden/dimmed enemy grid outline
        self._draw_dimmed_enemy_grid(screen)
        
        # Draw Ships
        for ship in self.sys.dock.get_placed_ships():
            self._draw_ship(screen, ship)
            
        for ship in self.sys.dock.get_unplaced_ships():
            self._draw_dock_ship(screen, ship)
            
        # Draw dragged ship + Preview
        if self.sys.drag_controller.is_dragging:
            ship = self.sys.drag_controller.selected_ship
            x = self.mouse_pos[0] - self.sys.drag_controller.mouse_offset_x
            y = self.mouse_pos[1] - self.sys.drag_controller.mouse_offset_y
            self._draw_preview(screen, ship, x, y)
            
            # Draw actual dragged ship
            w = ship.length * CELL_SIZE if ship.orientation == "H" else CELL_SIZE
            h = CELL_SIZE if ship.orientation == "H" else ship.length * CELL_SIZE
            pygame.draw.rect(screen, BLUE, (x, y, w, h))
            pygame.draw.rect(screen, WHITE, (x, y, w, h), 2)
            
            # Draw segment lines for dragged
            for i in range(ship.length):
                sx = x + (i * CELL_SIZE if ship.orientation == "H" else 0)
                sy = y + (i * CELL_SIZE if ship.orientation == "V" else 0)
                pygame.draw.rect(screen, WHITE, (sx, sy, CELL_SIZE, CELL_SIZE), 1)

        # Draw Buttons
        self.btn_auto.draw(screen)
        self.btn_reset.draw(screen)
        self.btn_start.draw(screen)

        hint = pygame.font.SysFont(None, 24).render("ESC - Back", True, GRAY)
        screen.blit(hint, (SCREEN_WIDTH - hint.get_width() - MARGIN, 14))

    def _draw_grid(self, screen, offset_x, label):
        # Draw label
        txt = self._font_header.render(label, True, WHITE)
        screen.blit(txt, (offset_x, MARGIN - 35))
        
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = offset_x + c * CELL_SIZE
                y = MARGIN + r * CELL_SIZE
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def _draw_dimmed_enemy_grid(self, screen):
        # Draw label
        txt = self._font_header.render("SHIP DOCK", True, GRAY)
        screen.blit(txt, (ENEMY_OFFSET, MARGIN - 35))
        
        # Dimmed representation of where enemy grid normally is, just to keep UI balanced
        # Or we use it for Ship Dock boundary as specified.

    def _draw_ship(self, screen, ship):
        rect = self._get_ship_rect(ship)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)
        for i in range(ship.length):
            sx = rect.x + (i * CELL_SIZE if ship.orientation == "H" else 0)
            sy = rect.y + (i * CELL_SIZE if ship.orientation == "V" else 0)
            pygame.draw.rect(screen, WHITE, (sx, sy, CELL_SIZE, CELL_SIZE), 1)

    def _draw_dock_ship(self, screen, ship):
        rect = self._get_dock_rect(ship)
        pygame.draw.rect(screen, GRAY, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)
        for i in range(ship.length):
            sx = rect.x + (i * CELL_SIZE if ship.orientation == "H" else 0)
            sy = rect.y + (i * CELL_SIZE if ship.orientation == "V" else 0)
            pygame.draw.rect(screen, WHITE, (sx, sy, CELL_SIZE, CELL_SIZE), 1)

    def _draw_preview(self, screen, ship, x, y):
        # Check if perfectly snapped in grid
        cell_center_x = x + CELL_SIZE // 2
        cell_center_y = y + CELL_SIZE // 2
        
        grid_rect = pygame.Rect(PLAYER_OFFSET, MARGIN, GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
        if not grid_rect.collidepoint(cell_center_x, cell_center_y):
            return # outside
            
        col = (cell_center_x - PLAYER_OFFSET) // CELL_SIZE
        row = (cell_center_y - MARGIN) // CELL_SIZE
        
        # Auto-push boundaries visually
        if ship.orientation == "H" and col + ship.length > GRID_SIZE:
            col = GRID_SIZE - ship.length
        if ship.orientation == "V" and row + ship.length > GRID_SIZE:
            row = GRID_SIZE - ship.length
        
        # Create preview surface with alpha
        w = ship.length * CELL_SIZE if ship.orientation == "H" else CELL_SIZE
        h = CELL_SIZE if ship.orientation == "H" else ship.length * CELL_SIZE
        preview = pygame.Surface((w, h), pygame.SRCALPHA)
        
        is_valid = self.sys.check_valid_placement(row, col, ship)
        color = (*GREEN, 128) if is_valid else (*RED, 128)
            
        preview.fill(color)
        px = PLAYER_OFFSET + col * CELL_SIZE
        py = MARGIN + row * CELL_SIZE
        screen.blit(preview, (px, py))
