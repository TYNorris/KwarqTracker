import asyncio

from app.src import Singleton
from app.src.reader import IReader, get_reader

class Broker(Singleton):

    def __init__(self):
        super().__init__()
        if "is_running" in self.__dict__:
            return

        self.reader = get_reader()
        self.reader.add_listener(self.on_new_tag)
        self.message = ""
        self.is_running = True

    def get_current_message(self):
        return self.message

    def on_new_tag(self, tag: int):
        self.message = tag

    async def loop(self):
        while True:
            await asyncio.sleep(0.5)
            self.reader.read_once()



