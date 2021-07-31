import asyncio
from datetime import datetime

from app.src import Singleton
from app.src.reader import get_reader
from app.src.storage.helper import StorageHelper
from .user import User
from .message import Message, Status


class Broker(Singleton):

    def __init__(self):
        super().__init__()
        if "is_running" in self.__dict__:
            return
        self._coroutines = []

        self.reader = get_reader()
        self.storage = StorageHelper()
        self.reader.add_listener(self.on_new_tag)
        self.message = Message.default()
        self.is_running = True
        self._last_tag = 0

    def get_current_message(self) -> Message:
        return self.message

    def get_last_tag(self) -> int:
        return self._last_tag

    def add_user(self, name: str, uid: int):
        self.storage.add_user(User(uid, name))

    def on_new_tag(self, tag: int):
        if tag is None or tag == self._last_tag:
            return
        self._last_tag = tag
        user = self.storage.get_user(tag)

        if user is None:
            self.message = Message(
                title=f"Whoops! Unknown user",
                subtitle=f"Id: {tag}",
                status=Status.fail
            )
        else:
            user.attended(date=datetime.now())
            self.storage.update_user(user)
            self.message = Message(
                title=f"Welcome {user.name}!",
                subtitle=f"You've attended {user.get_attendance_count()} times.",
                status=Status.success
            )

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
        self.message = Message.default()
