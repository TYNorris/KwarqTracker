import asyncio
from threading import Thread

from app.src.config import get_config
from app.src.logger.logger import setup_logger
from app.src.frontend import server
from app.src.user.broker import Broker

app = server.app

setup_logger()
config = get_config()


def reader_start():
    asyncio.run(Broker().loop())

reader_thread = Thread(target=reader_start)
reader_thread.start()


if __name__ == '__main__':
    server.app.run_server(
        host="0.0.0.0",
        port="8050",
    )
