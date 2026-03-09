# Battleship AI Difficulty System

You are an experienced Python game developer working on a Battleship game implemented in **Python + Pygame**.

The project already has a clean architecture with the following systems:

* Engine
* StateManager
* EventManager
* Game (core logic)
* Board
* Ship
* PlacementSystem
* SQLite database

Your task is to design and implement a **three-level AI difficulty system** for the enemy player.

The AI must be modular, maintainable, and compatible with the existing architecture.

---

# AI Difficulty Levels

The game must support three difficulty levels:

Easy
Medium
Hard

Each difficulty level must use a **different AI strategy**.

---

# AI Architecture

Use the **Strategy Pattern**.

Create a base AI interface and separate strategy classes.

Example structure:

entities/
ai/
base_ai.py
random_ai.py
hunt_target_ai.py
probability_ai.py

---

# Base AI Class

Create a base class that defines the interface for all AI strategies.

Responsibilities:

* select the next attack coordinate
* track previous attacks
* receive board feedback (hit, miss, sunk)

Example responsibility:

choose_attack(board)

The AI should only interact with the **enemy board state**, not rendering systems.

---

# Easy Difficulty – Random AI

Strategy:

Randomly attack any grid cell that has not been attacked before.

Rules:

* do not attack the same cell twice
* choose from remaining valid cells

Behavior:

This AI should feel simple and unpredictable but not intelligent.

---

# Medium Difficulty – Hunt and Target AI

This AI operates in two modes.

HUNT MODE

The AI searches the board for ships.

Use a **checkerboard pattern** to reduce search space.

Example:

X . X . X
. X . X .
X . X . X

Ships longer than one cell cannot avoid this pattern.

---

TARGET MODE

When a ship is hit:

1. switch to target mode
2. attack adjacent cells (up, down, left, right)
3. determine ship orientation
4. continue attacking along the detected direction

Return to hunt mode when the ship is sunk.

---

# Hard Difficulty – Probability AI

Implement a **probability density algorithm**.

Goal:

Calculate the most likely location of remaining ships.

Steps:

1. iterate through all possible ship placements
2. skip placements that conflict with known misses
3. skip placements that contradict known hits
4. increment probability scores for cells covered by valid placements

Create a probability map of the board.

Example:

1 2 5 6 4
2 5 9 7 3
1 3 6 4 2

The AI attacks the cell with the highest probability.

This AI should be significantly harder to beat.

---

# Difficulty Selection

The game should allow selecting AI difficulty before the match starts.

Example:

Easy → RandomAI
Medium → HuntTargetAI
Hard → ProbabilityAI

The Game class should interact with the AI through a common interface.

Example:

ai.choose_attack(board)

The Game class must not depend on a specific AI implementation.

---

# Architectural Rules

AI logic must remain part of the **entities layer**.

AI modules must not import:

pygame
UI modules
State classes

AI must only work with:

board state
attack history
ship status

---

# Performance Constraints

The board is 10x10.

AI calculations must remain efficient.

Probability calculations should complete within a single frame.

---

# Optional Improvements

Consider adding:

* AI thinking delay (0.5–1.5 seconds)
* debug visualization of probability heatmap
* logging AI decisions for testing

---

The final implementation must remain consistent with the project's architecture rules and separation of concerns.
