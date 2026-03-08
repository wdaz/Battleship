# Battleship Game Architecture Documentation

This document serves as a comprehensive guide for AI assistants and developers to understand the structural design, core systems, and architectural patterns of the Battleship project.

## 1. High-Level Architecture

The game strictly separates rendering (View/State) from pure game rules (Model/Logic). The entry point is `src/main.py`, which initializes the main controller, the `Engine`.

### Key Relationships (Dependency Tree)
```text
Engine (Main Controller)
  ├── StateManager (FSM for UI/Screens)
  │   └── BaseState Subclasses (MainMenu, Gameplay, Pause, GameOver)
  ├── EventManager (Pub/Sub Event Bus)
  ├── Game (Pure Game Logic)
  │   ├── Board (Player)
  │   │   └── Ships (Collection)
  │   ├── Board (Enemy)
  │   │   └── Ships (Collection)
  │   └── SimpleAI (Enemy behavior)
  └── Database (Persistence via SQLite)
```

## 2. Core Layers & Systems

### A. Application Layer (`src/core/engine.py`)
- **Engine**: The primary application controller. It manages the global Pygame window, the game loop, ticking FPS, and dispatching events.
- **Save/Load**: The Engine manages snapshot-based saving and loading of the `Game` state to and from the `Database`.

### B. State Management (`src/core/state_manager.py` & `src/states/*`)
- **Finite State Machine (FSM)**: Uses a stack-based approach supporting overlay states.
  - `change(name)`: Replaces the current state completely.
  - `push(name)`: Overlays a state (e.g., Pause menu over Gameplay).
  - `pop()`: Returns to the previously active state.
- **BaseState**: Provides the lifecycle template for all states (`enter`, `exit`, `handle_events`, `update`, `draw`).

### C. Game Logic Layer (`src/core/engine.py` / `src/entities/`)
- **Game**: Handles pure game rules, managing turn state ("player" vs "computer") and coordinating between the two boards. Contains no rendering logic.
- **Board (`entities/board.py`)**: Stores `Ship` objects, manages valid placements, tracks hits/misses via coordinate sets, and determines win conditions (`all_sunk()`).
- **Ship (`entities/ship.py`)**: A simple data container tracking its given coordinates and hit coordinates.
- **SimpleAI (`entities/enemy.py`)**: Uses the Strategy Pattern for enemy decision making. Currently randomly selects valid, unattacked grid coordinates.

### D. Support Systems
- **EventManager (`src/core/events.py`)**: Implements a Pub/Sub pattern allowing decoupled communication. Subsystems `subscribe` to events and `emit` them globally.
- **Database (`src/core/database.py`)**: The persistence layer using SQLite (`battleship.db`). Stores user profiles and JSON-serialized snapshots of game states for saving/resuming games.
- **Settings (`src/settings.py`)**: Global configuration including grid dimensions (10x10), cell sizes (40px), rendering colors, and FPS caps.

## 3. Crucial Architectural Conventions

When modifying this codebase, strictly adhere to these patterns:

1. **Separation of Concerns (Logic vs. Rendering)**:
   - NEVER place Pygame drawing logic (`pygame.draw`, `surface.blit`) inside `src/entities/` or `src/core/` (except inside custom UI utilities).
   - Display logic belongs exclusively within `src/states/` subclasses.
2. **State Pattern**: UI screens transition via the `StateManager`. Any new UI view requires a new state class inheriting from `BaseState`.
3. **Event-Driven Communication**: For cross-component communication (especially from deep within the logic layer back up to the UI), emit an event via `EventManager` instead of tightly coupling classes.
4. **Coordinate System**: The game operates primarily on `(row, col)` tuples for grid logic, mapping to Pygame pixel coordinates `(x, y)` only within the rendering state layers.