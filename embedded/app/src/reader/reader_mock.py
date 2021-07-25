from .i_reader import IReader
from app.src.storage import demo_users

class ReaderMock(IReader):
    _count = 0
    _index = 0

    def __init__(self):
        super().__init__()

    def read_once(self):
        self._count += 1
        if self._count % 25 == 0:
            uid = list(demo_users.keys())[self._index]
            self.event.on_change(uid)

            self._index += 1
            if self._index >= len(demo_users):
                self._index = 0

            return uid
        return None

    def close(self):
        pass
