class BaseState:
    """Abstract base class for all game states."""

    def __init__(self, engine):
        self.engine = engine

    def enter(self):
        """Called when the state becomes active."""

    def exit(self):
        """Called when the state is replaced."""

    def handle_events(self, events):
        """Process a list of pygame events."""

    def update(self):
        """Update game logic for this frame."""

    def draw(self, screen):
        """Render the state to the screen."""