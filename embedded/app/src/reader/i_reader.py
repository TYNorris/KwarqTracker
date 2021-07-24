from events.events import Events

from abc import ABC, abstractmethod

class IReader(ABC):
    LAST_TAG = ""

    def __init__(self):
        super().__init__()
        self.event = Events()

    def add_listener(self, callback):
        self.event.on_change += callback

    def remove_listener(self, callback):
        self.event.on_change -= callback

    @abstractmethod
    def read_once(self):
        return None

    @abstractmethod
    def close(self):
        pass
