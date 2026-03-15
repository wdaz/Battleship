# Battleship - User Guide

Welcome to **Battleship**! This guide will walk you through the controls, gameplay mechanics, and features of the game.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Controls](#controls)
3. [Game Phases](#game-phases)
    - [Main Menu](#main-menu)
    - [Ship Placement](#ship-placement)
    - [The Battle](#the-battle)
4. [Pause & Saving](#pause--saving)

---

## Getting Started

To launch the game, open your terminal, activate your virtual environment, and run the main script:

```bash
python src/main.py
```

*(If you are using the `.venv` folder on Windows, you can also run: `.venv/Scripts/python.exe src/main.py`)*

---

## Controls

### Mouse

- **Left Click**:
  - Navigate menus and click buttons.
  - Pick up, drag, and drop ships from the Ship Dock to your grid.
  - Fire an attack at a specific cell on the enemy's grid.

- **Right Click**:
  - Rotate a ship while dragging it during the Ship Placement phase.

### Keyboard

- **R Key**: Rotate a ship while you are dragging it.

- **ESC Key**:
  - During Ship Placement: Return to the Main Menu.
  - During Gameplay: Pause the game and open the Pause Menu.
  - Inside Pause Menu: Resume the game.
- **Arrow Keys (Up/Down)**: Navigate through menu buttons (e.g., Pause Menu, Game Over Menu).
- **Enter Key**: Select the currently highlighted menu button.

---

## Game Phases

### 1. Main Menu

When you drop into the game, you will see the Main Menu. Here you can:

- **Select Difficulty**: Choose between *Easy* (Random firing), *Medium* (Hunt & Target logic), or *Hard* (Probability-based tracking) AI.
- **Load Game**: If you previously saved a game, you can load your progress from here.
- **Start**: Begin a new game and head to the Ship Placement grid.

### 2. Ship Placement

Before the battle begins, you must position your fleet.

- **Manual Placement**: Left-click and drag ships from the "SHIP DOCK" onto your "PLAYER" grid. Use **Right Click** or **R** to rotate them vertically or horizontally.
- **Auto Arrange**: Click the `AUTO ARRANGE` button if you want the computer to instantly randomize your ship positions.
- **Reset**: Made a mistake? Click `RESET` to return all ships back to the dock.
- **Start Battle**: Once every single ship is placed on the board, the `START BATTLE` button will activate. Click it to deploy your fleet!

### 3. The Battle

You and the Computer will take turns firing at each other's grids.

- **Your Turn**: Left-click anywhere on the **ENEMY** grid (right side) to fire a missile.
  - A **Red Circle** indicates a "Hit".
  - A **Blue Circle** indicates a "Miss".
- **Enemy Turn**: The computer will automatically fire at your grid shortly after your turn ends. Watch your grid carefully to see if your ships are taking damage.

The game ends when either you or the computer successfully sinks all of the opponent's ships. A pop-up will appear announcing the winner, allowing you to instantly start a **New Game** or return to the **Main Menu**.

---

## Pause & Saving

Need to take a break?

1. Press the **ESC** key during battle to bring up the **Pause Menu**.
2. From here, you can click **Resume** to get back into the action.
3. If you need to close the game, click **Save & Main Menu**. The game will automatically take a snapshot of your current board, whose turn it is, and the AI's memory. You can continue this exact match later by clicking "Load" on the Main Menu!
