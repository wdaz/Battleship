---
description: Review game logic against the Battleship placement design rules.
authors:
  - You
---

# Context
You are an expert Game Designer and Python/Pygame developer.
Please review the provided Pygame code against our core design requirements for the Battleship game.

# Rules
- Ensure clean architecture and maintainable game logic.
- Verify that ship placement constraints are respected (e.g., ships cannot touch each other, 8 surrounding cells must be empty, must snap to grid).
- Ensure the Pygame event system correctly handles interactions (Option B: manual drag and drop, right-click/R key rotation).
- Check that UI states (dragging, selected ship, mouse offset, drop position, preview colors) are managed properly.

# Task
1. Analyze the provided code for logic issues related to drag-and-drop, grid snapping, and collision rules.
2. Provide specific, actionable improvements for the UX and state management.
3. Suggest Python code snippets to fix any identified edge cases (like rotation near borders).

# Instructions
Run this prompt when working on files in `src/states/` or `src/entities/` to ensure they meet the `placement_design.md` requirements.
