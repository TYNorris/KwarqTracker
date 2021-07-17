from .i_reader import IReader


class ReaderMock(IReader):
    _count = 0

    def __init__(self):
        super().__init__()

    def read_once(self):
        self._count += 1
        if self._count % 5 == 0:
            return f"MOCK_TAG{self._count}"
        return None

    def close(self):
        pass
