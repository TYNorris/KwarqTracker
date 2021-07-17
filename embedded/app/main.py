import asyncio
from threading import Thread

from datetime import datetime

from embedded.app.src.config import get_config
from embedded.app.src.logger.logger import setup_logger
from embedded.app.src.frontend import server
from embedded.app.src.reader import get_reader

config = get_config()
reader = get_reader()

async def reader_async():
    while True:
        await asyncio.sleep(1)
        tag = reader.read_once()
        if tag is None:
            continue
        reader.LAST_TAG = tag
        print(f'Updated Tag: {tag}')


def reader_start():
    asyncio.run(reader_async())

reader_thread = Thread(target=reader_start)


if __name__ == '__main__':
    setup_logger()
    reader_thread.start()
    server.app.run_server()
