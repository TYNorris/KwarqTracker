from .i_reader import IReader


class ReaderMock(IReader):
    _count = 0

    def __init__(self):
        super().__init__()

    def read_once(self):
        self._count += 1
        if self._count % 5 == 0:
            tag = 19088700 + self._count
            self.event.on_change(tag)
            return tag
        return None

    def close(self):
        pass
