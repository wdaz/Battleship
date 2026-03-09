# Battleship Engine Architecture Documentation

This document outlines the formal architecture of the custom game engine used in this Battleship repository. The engine is built using Pygame but employs an architecture that heavily decouples pure game logic from rendering and input handling.

## 1. The Game Loop

The core orchestration happens within the `Engine` and `Game` classes in `src/core/engine.py`. This setup relies on a classic **3-phase frame cycle**: Input $\rightarrow$ Update $\rightarrow$ Render.

### `Engine` Class
The `Engine` manages the application lifecycle, owns the Pygame window, and maintains instances of the `StateManager` and `EventManager`. 

The `run()` method processes the game loop at a fixed FPS:
```python
def run(self):
    self.running = True
    self.state_manager.change("main_menu")
    
    while self.running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        # Phase 1: Input Routing
        self.state_manager.handle_events(events)
        
        # Phase 2: Game Logic Update
        self.state_manager.update()
        
        # Phase 3: Render Frame
        self.state_manager.draw(self.screen)
        
        pygame.display.flip()
        self.clock.tick(FPS)
```

### `Game` Class
The `Game` class acts as a **pure game-logic container**. It sits completely independent of Pygame rendering. It holds the player and enemy boards, turn tracking (`"player"` or `"computer"`), and evaluates the AI's attack logic. This clear separation makes serializing the game state (saving/loading) straightforward through methods like `game_to_snapshot()` and `load_game_snapshot()`.

## 2. State Management

The `StateManager` (found in `src/core/state_manager.py`) operates as a **finite-state machine (FSM) with a stack**. 

Rather than defining game sequences inside a single massive loop, the application delegates `handle_events()`, `update()`, and `draw()` out to self-contained State objects (e.g., `main_menu`, `gameplay`, `pause`).

### Core Methods
* **`change(name)`**: Executes a complete transition. It clears the overlay stack, calls `exit()` on the old state, and `enter()` on the new state.
* **`push(name)`**: Retains the current state in a stack and layers a new state on top. This is extremely useful for displaying a pause menu overlay without losing gameplay progress.
* **`pop()`**: Removes the overlay, returning execution control to the previous state.

## 3. Event System

To facilitate decoupled communication across different parts of the architecture (like UI buttons signaling the Engine, or an entity signaling an audio trigger), the game uses an `EventManager` (`src/core/events.py`). 

This operates on a fundamental **Publish/Subscribe pattern**:
```python
# Subscription
event_manager.subscribe("ship_hit", on_ship_hit_handler)

# Emission
event_manager.emit("ship_hit", ship=target_ship, cell=(3, 5))
```
States, interfaces, and game objects can execute cross-system logic without holding direct references to each other. 

## 4. AI Integration

The AI integration elegantly demonstrates the engine's decoupling. The `Game` class does not hardcode enemy behavior; rather, it interacts with an AI instance derived from the abstract `BaseAI` class (`src/entities/ai/base_ai.py`).

```python
class BaseAI(ABC):
    @abstractmethod
    def choose_attack(self, board):
        pass
```

During a computer turn, the engine simply calls `self.ai.choose_attack(self.player)` which hands over the targeted cell coordinate. Strategies like `RandomAI` (Easy), `HuntTargetAI` (Medium), and `ProbabilityAI` (Hard) can be swapped seamlessly based on difficulty without modifying the game loop or board entities.

## 5. Architecture Analysis (Pros vs. Cons)

| **Aspect** | **Pros** | **Cons** |
|-----------|---------|---------|
| **Decoupling** | Pure game logic (`Game`) is fully isolated from Pygame rendering and input logic. This makes unit testing, saving state (snapshots), and code reuse incredibly easy. | Using the `EventManager` for critical game state changes can make the precise execution order hard to track and debug. |
| **State Management** | Using a stack (`push`/`pop`) for states handles overlays (like the Pause menu) cleanly, maintaining clear `enter()`/`exit()` lifecycles. | There is no built-in way to pass parameters directly through state transitions (e.g., `change("game_over", winner="player")`). Data must be dumped globally or passed via events. |
| **Event System** | Extremely loose coupling. It allows UI elements or sound effect managers to hook into game actions seamlessly. | Lack of type-safety. It is easy to emit events with typos that no one listens to. Furthermore, there is no built-in error handling if a listener crashes. |
| **Modularity & Scaling**| Adding a new screen (e.g., a "Credits" screen) just requires building a new `BaseState` and registering it. AI strategies can be cleanly swapped. | The main `Engine` holds centralized references to the state, events, and the game itself. As the project scales, it risks becoming a tightly coupled "God Object". |