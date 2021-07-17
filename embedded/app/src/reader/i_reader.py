from abc import ABC, abstractmethod

class Singleton:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class IReader(Singleton, ABC):
    LAST_TAG = ""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def read_once(self):
        return None

    @abstractmethod
    def close(self):
        pass
