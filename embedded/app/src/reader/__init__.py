import platform
from .i_reader import IReader


def get_reader() -> IReader:
    if platform.system() == 'Windows':
        from .reader_mock import ReaderMock
        return ReaderMock()
    from .reader import Reader
    return Reader()
