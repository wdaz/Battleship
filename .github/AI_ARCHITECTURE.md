# Battleship Game – AI Architecture Guide

This document describes the architecture and development rules of the Battleship project.
It is written primarily for **AI coding assistants** (Copilot, ChatGPT, Cursor) to understand the structure of the codebase.

The architecture enforces **strict separation between game logic, UI rendering, and interaction systems**.

---

# 1. Application Entry Point

Entry file:

```
src/main.py
```

The application initializes the **Engine**, which controls the main loop and global systems.

Main loop responsibilities:

* handle pygame events
* update active game state
* render current state
* control FPS

---

# 2. High-Level System Architecture

```
Engine
 ├── StateManager
 │   └── BaseState subclasses
 │       ├── MainMenuState
 │       ├── ShipPlacementState
 │       ├── GameplayState
 │       ├── PauseState
 │       └── GameOverState
 │
 ├── EventManager
 │
 ├── Game (Pure Game Logic)
 │   ├── Board
 │   │   └── Ship
 │   └── SimpleAI
 │
 ├── PlacementSystem
 │   ├── AutoPlacement
 │   ├── DragController
 │   ├── PlacementValidator
 │   └── ShipDock
 │
 └── Database
```

---

# 3. Game Flow

Game phases:

```
Main Menu
    ↓
Ship Placement Phase
    ↓
Battle Phase
    ↓
Game Over
```

### Ship Placement Phase

Players arrange ships before battle.

Supported features:

* automatic ship placement
* drag-and-drop ship placement
* ship rotation
* board reset

The battle cannot start until **all ships are placed**.

---

# 4. State System

The UI layer uses a **stack-based finite state machine**.

Implemented in:

```
src/core/state_manager.py
```

State transitions:

```
change(state)
push(state)
pop()
```

State lifecycle:

```
enter()
exit()
handle_events()
update()
draw()
```

States handle **all rendering and user interaction**.

---

# 5. Game Logic Layer

Located in:

```
src/entities/
```

This layer contains **pure gameplay rules**.

### IMPORTANT RULE

Game logic **must not import or use pygame rendering functions**.

No usage of:

```
pygame.draw
pygame.Surface.blit
pygame.display
```

inside entities or core logic.

---

## Game

Central gameplay controller.

Responsibilities:

* manage player and enemy turns
* coordinate both boards
* resolve attacks
* determine win conditions

---

## Board

Represents a 10×10 grid.

Stores:

```
ships
hit_coordinates
miss_coordinates
```

Responsibilities:

* place ships
* register attacks
* detect ship destruction
* check if all ships are sunk

---

## Ship

Data object representing a ship.

Stores:

```
length
coordinates
orientation
hit_coordinates
```

Responsibilities:

* track hits
* determine sunk state

---

## SimpleAI

Enemy behavior controller.

Current strategy:

```
random valid cell targeting
```

Future strategies may include:

* hunt targeting
* probability heatmap targeting

---

# 6. Placement System

Handles ship arrangement before the game starts.

Located in:

```
src/placement/
```

This system is responsible for **interaction logic**, not rendering.

---

## PlacementSystem

Coordinator for placement features.

Responsibilities:

* manage ship dock
* coordinate drag operations
* call placement validator
* trigger auto placement

---

## AutoPlacement

Generates random valid ship layouts.

Algorithm pattern:

```
for each ship
    choose random orientation
    choose random start cell
    validate placement
    retry if invalid
```

Placement rules:

* ships must stay inside board
* ships cannot overlap
* ships cannot touch

---

## DragController

Handles mouse-based ship movement.

Tracks:

```
selected_ship
dragging_state
mouse_offset
preview_cells
```

Interaction flow:

```
mouse down → select ship
mouse move → update drag position
mouse up → attempt placement
```

Invalid placements return ships to the dock.

---

## PlacementValidator

Validates ship placement rules.

Checks:

```
inside board
no overlap
no touching ships
```

Touch detection requires checking **8 neighboring cells**.

---

## ShipDock

Represents ships waiting to be placed.

Example fleet:

```
1 ship length 4
2 ships length 3
3 ships length 2
4 ships length 1
```

Responsibilities:

* provide ships for dragging
* remove ships when placed
* restore ships when reset

---

# 7. Event System

Located in:

```
src/core/events.py
```

Implements a **publish/subscribe event bus**.

Purpose:

* decouple UI and logic systems
* allow cross-system communication

Example events:

```
SHIP_DRAG_STARTED
SHIP_DROPPED
SHIP_PLACED
AUTO_PLACEMENT_REQUEST
PLACEMENT_RESET
ATTACK_RESOLVED
GAME_OVER
```

---

# 8. Database System

Located in:

```
src/core/database.py
```

Uses **SQLite**.

Stored data:

* player profiles
* saved games
* serialized game snapshots

Game state is stored as **JSON snapshots**.

---

# 9. Global Settings

Located in:

```
src/settings.py
```

Contains constants such as:

```
GRID_SIZE = 10
CELL_SIZE = 40
FPS = 60
```

Rendering colors and UI constants are also defined here.

---

# 10. Coordinate System

Game logic uses:

```
(row, col)
```

Rendering states convert these into pixel positions:

```
(x, y)
```

Conversion must occur **only inside state rendering code**.

---

# 11. Architectural Rules

AI assistants must follow these rules when modifying the codebase.

### Rule 1 — Logic vs Rendering

Never place rendering code inside:

```
src/entities
src/core
src/placement
```

Rendering belongs only to:

```
src/states
```

---

### Rule 2 — State-Based UI

Every new screen must be implemented as a **State**.

Examples:

```
MainMenuState
ShipPlacementState
GameplayState
```

---

### Rule 3 — Event-Based Communication

Avoid tight coupling between systems.

Use the EventManager instead.

---

### Rule 4 — Game Logic Purity

Game logic must remain deterministic and testable.

Do not introduce UI or rendering dependencies into the logic layer.
