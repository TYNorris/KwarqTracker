import asyncio
from datetime import datetime

from app.src import Singleton
from app.src.reader import IReader, get_reader
from app.src.storage.helper import StorageHelper

class Broker(Singleton):

    def __init__(self):
        super().__init__()
        if "is_running" in self.__dict__:
            return
        self._coroutines = []

        self.reader = get_reader()
        self.storage = StorageHelper()
        self.reader.add_listener(self.on_new_tag)
        self.message = ""
        self.is_running = True

    def get_current_message(self):
        return self.message

    def on_new_tag(self, tag: int):
        user = self.storage.get_user(tag)

        if user is None:
            self.message = f'Unknown user! id: {tag}'
        else:
            user.attended(date=datetime.now())
            self.message = f'Welcome {user.name}! You\'ve attended {user.attendance_count} times.'

        task = asyncio.create_task(asyncio.sleep(5))
        self._coroutines.append(task)

    async def read_loop(self):
        while True:
            await asyncio.sleep(0.5)
            self.reader.read_once()

    async def clear_loop(self):
        while True:
            if not self._coroutines:
                await asyncio.sleep(1)
                continue
            done, pending = await asyncio.wait(self._coroutines, return_when=asyncio.ALL_COMPLETED)
            self._coroutines.clear()
            self._clear_message()

    async def loop(self):
        await asyncio.gather(
            self.read_loop(),
            self.clear_loop(),
        )

    def _clear_message(self):
        self.message = ""
