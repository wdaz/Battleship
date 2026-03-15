import os
import sys
import pytest
import pygame

# Add the 'src' directory to the Python path so we can import from it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from core.engine import Engine
from settings import ENEMY_OFFSET, MARGIN, CELL_SIZE

def render_and_wait(engine, delay=1000):
    pygame.event.pump()
    engine.state_manager.draw(engine.screen)
    pygame.display.flip()
    pygame.time.delay(delay)

def test_full_game_flow():
    # Initialize Engine
    engine = Engine()
    
    # Check if State Manager initialized properly
    assert engine.state_manager is not None

    # Step 1: Force state to 'ship_placement'
    engine.state_manager.change("ship_placement")
    placement_state = engine.state_manager._current
    
    render_and_wait(engine, 1000)
    
    # Assert we are in the correct state
    assert type(placement_state).__name__ == "ShipPlacementState"
    
    # Currently Start Battle button should be disabled because ships aren't placed
    assert placement_state.btn_start.enabled == False

    # Step 2: Simulate clicking 'AUTO ARRANGE'
    # We grab the button's exact center to guarantee a hit
    auto_btn_center = placement_state.btn_auto.rect.center
    
    event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': auto_btn_center})
    event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': auto_btn_center})
    
    # Route simulation events through the state manager
    engine.state_manager.handle_events([event_down, event_up])
    
    render_and_wait(engine, 1000)
    
    # The 'START BATTLE' button should now be enabled since all ships are placed
    assert placement_state.btn_start.enabled == True

    # Step 3: Simulate clicking 'START BATTLE'
    start_btn_center = placement_state.btn_start.rect.center
    
    event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': start_btn_center})
    event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': start_btn_center})
    engine.state_manager.handle_events([event_down, event_up])
    
    render_and_wait(engine, 1000)
    
    # Verify state transition to 'gameplay'
    gameplay_state = engine.state_manager._current
    assert type(gameplay_state).__name__ == "GameplayState"
    
    # Game data should be populated
    game = engine.game
    assert game is not None
    assert game.turn == "player"
    
    # Confirm the player really has their ships placed
    assert len(game.player.ships) > 0
    assert len(game.enemy.ships) > 0

    # Step 4: Simulate Gameplay Attack on Enemy Board
    # We will "click" the top-left cell of the enemy board -> Grid(0, 0)
    top_left_cell_center = (ENEMY_OFFSET + CELL_SIZE // 2, MARGIN + CELL_SIZE // 2)
    
    attack_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': top_left_cell_center})
    engine.state_manager.handle_events([attack_down])
    
    render_and_wait(engine, 1000)
    
    # Validate that an attack was registered on the enemy's board
    assert len(game.enemy.attacks) == 1
    assert (0, 0) in game.enemy.attacks
    
    # Finally, simulate pushing "ESC" to Pause the game
    esc_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE})
    engine.state_manager.handle_events([esc_event])
    
    render_and_wait(engine, 1000)
    
    # Since pause is a stack push, the current state should be 'PauseState' 
    # but the previous one should still be beneath it.
    pause_state = engine.state_manager._current
    assert type(pause_state).__name__ == "PauseState"

    pygame.quit()

def test_player_wins():
    engine = Engine()
    engine.state_manager.change("ship_placement")
    placement_state = engine.state_manager._current
    
    auto_btn_center = placement_state.btn_auto.rect.center
    engine.state_manager.handle_events([
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': auto_btn_center}),
        pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': auto_btn_center})
    ])
    
    start_btn_center = placement_state.btn_start.rect.center
    engine.state_manager.handle_events([
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': start_btn_center}),
        pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': start_btn_center})
    ])

    game = engine.game
    all_enemy_cells = []
    for ship in game.enemy.ships:
        for c in ship.cells:
            all_enemy_cells.append(c)
            
    last_cell_r, last_cell_c = all_enemy_cells.pop()
    
    for c in all_enemy_cells:
        game.enemy.receive_attack(c)
        
    render_and_wait(engine, 1000)
    
    click_pos = (ENEMY_OFFSET + last_cell_c * CELL_SIZE + CELL_SIZE // 2, 
                 MARGIN + last_cell_r * CELL_SIZE + CELL_SIZE // 2)
    
    attack_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': click_pos})
    engine.state_manager.handle_events([attack_down])
    
    engine.state_manager.update()
    render_and_wait(engine, 2000)
    
    assert engine.game_over_winner == "player"
    pygame.quit()


def test_computer_wins():
    engine = Engine()
    engine.state_manager.change("ship_placement")
    placement_state = engine.state_manager._current
    
    auto_btn_center = placement_state.btn_auto.rect.center
    engine.state_manager.handle_events([
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': auto_btn_center}),
        pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': auto_btn_center})
    ])
    
    start_btn_center = placement_state.btn_start.rect.center
    engine.state_manager.handle_events([
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': start_btn_center}),
        pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': start_btn_center})
    ])

    game = engine.game
    
    for ship in game.player.ships:
        for c in ship.cells:
            game.player.receive_attack(c)
            
    engine.state_manager.update()
    render_and_wait(engine, 2000)
    
    assert engine.game_over_winner == "computer"
    pygame.quit()
