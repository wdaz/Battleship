You are an experienced Game Designer and Python/Pygame specialist. Your task is to design and implement the ship placement system for a Battleship game implemented in Python using Pygame.

The current game already has a working battle board with a **player grid and enemy grid**. Your task is to design and implement the **ship placement phase** that happens before the battle starts.

Focus on clean architecture, good UX, and maintainable game logic.

---

# Game Flow

The game should contain three phases:

1. Ship Placement Phase
2. Battle Phase
3. End Game Phase

During the **Ship Placement Phase**, the player can arrange ships and prepare for battle.

---

# Ship Placement Options

## 1. Automatic Ship Placement

Provide a button:

AUTO ARRANGE

Behavior:

* When the player clicks this button, ships are automatically placed on the board.
* Each click generates a **new random layout**.
* The player can press the button multiple times until they like the result.

Rules for automatic placement:

* Ships cannot overlap.
* Ships cannot touch each other (including diagonally).
* Ships must stay inside the grid.

Use a reliable algorithm to generate valid random ship layouts.

---

## 2. Manual Ship Placement (Option B)

Use **Option B placement system**.

Ships start in a **Ship Dock / Ship Panel**, not on the board.

Example ship inventory:

* 1 ship (4 cells)
* 2 ships (3 cells)
* 3 ships (2 cells)
* 4 ships (1 cell)

Ships are displayed in a panel next to the player board.

The player must drag ships from the dock onto the board.

---

# Drag and Drop System

Implement ship dragging using the Pygame event system.

Interaction flow:

1. Mouse click on ship → start dragging
2. Ship follows mouse movement
3. When released over the board:

   * convert mouse position to grid coordinates
   * attempt placement

If placement is invalid, the ship returns to the dock.

Track the following states:

* dragging state
* selected ship
* mouse offset
* drop position

---

# Grid Snap System

Ships must snap to grid cells.

Convert mouse coordinates into board cell positions.

Example flow:

mouse position → grid coordinate → calculate ship cells → validate placement → snap to grid.

---

# Ship Rotation

Ships must support orientation changes.

Allow two ways to rotate ships:

1. Right mouse click
2. Press the **R key**

Rotation switches between:

horizontal ↔ vertical

Handle edge cases when rotating near board borders.

If rotation causes overflow outside the grid, automatically adjust ship position.

---

# Placement Preview

When dragging a ship over the board, display a preview.

Preview colors:

Green → valid placement
Red → invalid placement

Before dropping the ship, validate:

* ship inside board
* no overlap with other ships
* ships do not touch each other

---

# Ship Collision Rules

Ships cannot touch each other.

Check the **8 surrounding cells** around each ship segment.

Example:

X X X
X S X
X X X

All surrounding cells must be empty.

---

# UI Controls

Add the following buttons:

AUTO ARRANGE
RESET
START BATTLE

RESET removes all ships and restores the ship dock.

START BATTLE is only enabled when **all ships are placed**.

---

# UI Layout

Design layout similar to:

PLAYER GRID | SHIP DOCK | ENEMY GRID

The Ship Dock shows remaining ships that must be placed.

---

# UX Improvements

Implement small UI improvements:

* ship hover highlight
* cell hover highlight
* snap animation when ship is placed
* visual feedback for hit and miss during battle

---

# Technical Challenges

Consider potential issues when implementing in Pygame:

* drag detection
* grid snapping
* rotation near edges
* placement validation
* board coordinate calculations

---

# Development Order

Implement features in this order:

1. placement phase state
2. auto placement system
3. ship dock
4. drag system
5. grid snapping
6. ship rotation
7. placement validation
8. placement preview highlighting
9. UI polish and animations

The result should be a clean, maintainable Pygame implementation with intuitive user interaction and modern game UX.
