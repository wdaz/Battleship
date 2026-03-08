class StateManager:
    """Finite-state machine that manages game screen transitions."""

    def __init__(self):
        self._states = {}
        self._current = None
        self._stack = []          # push/pop stack for overlay states (e.g. pause)

    def register(self, name, state):
        self._states[name] = state

    def change(self, name):
        """Replace the current state; clears the overlay stack."""
        self._stack.clear()
        if self._current is not None:
            self._current.exit()
        self._current = self._states[name]
        self._current.enter()

    def push(self, name):
        """Overlay *name* on top of the current state (current is NOT exited)."""
        self._stack.append(self._current)
        self._current = self._states[name]
        self._current.enter()

    def pop(self):
        """Return to the previous state without calling enter() on it."""
        if self._stack:
            self._current.exit()
            self._current = self._stack.pop()

    def handle_events(self, events):
        if self._current:
            self._current.handle_events(events)

    def update(self):
        if self._current:
            self._current.update()

    def draw(self, screen):
        if self._current:
            self._current.draw(screen)