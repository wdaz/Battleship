class EventManager:
    """Simple publish/subscribe event system."""

    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, callback):
        self._listeners.setdefault(event_type, []).append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)

    def emit(self, event_type, **data):
        for callback in self._listeners.get(event_type, []):
            callback(**data)