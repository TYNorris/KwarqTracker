import asyncio
import logging

from asyncio.queues import Queue
from datetime import datetime
from typing import List

from app.src import Singleton
from app.src.reader import get_reader
from app.src.storage.helper import StorageHelper
from app.src.email import Emailer
from .user import User
from .message import Message, Status


logger = logging.getLogger(__name__)


class Broker(Singleton):

    def __init__(self):
        super().__init__()
        logger.info("Starting Broker")
        if "is_running" in self.__dict__:
            return
        self._coroutines = []

        self.reader = get_reader()
        self.storage = StorageHelper()
        self.reader.add_listener(self.on_new_tag)
        self.message = Message.default()
        self.emailer = Emailer()
        self.is_running = True
        self._prevent_rescan = False
        self._is_email_queued = True
        self._incoming_queue = Queue()
        self._last_tag = 0

    def get_current_message(self) -> Message:
        return self.message

    def get_last_tag(self) -> int:
        return self._last_tag

    def get_all_users(self) -> List[User]:
        return self.storage.get_all_users()

    def add_user(self, name: str, uid: int):
        self.storage.add_user(User(uid, name))
        self.on_new_tag(uid)

    def on_new_tag(self, tag: int):
        if tag is None or (self._prevent_rescan and tag == self._last_tag):
            return
        self._last_tag = tag
        self._prevent_rescan = True
        self._incoming_queue.put_nowait(tag)

    def process_tag(self, tag: int):
        user = self.storage.get_user(tag)

        if user is None:
            self.message = Message(
                title=f"Whoops! Unknown user",
                subtitle=f"Id: {tag}",
                status=Status.fail
            )
        else:
            logger.info(f"CHECKIN - {user.name}, {user.uid}, {datetime.now().date()}")
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
            self._prevent_rescan = False
            self._clear_message()

    async def process_loop(self):
        while True:
            if self._incoming_queue.empty():
                await asyncio.sleep(0.1)
                continue
            tag = await self._incoming_queue.get()
            self.process_tag(tag)

    async def email_loop(self):
        while True:
            try:
                await asyncio.sleep(20)
                if self._is_email_queued:
                    self._is_email_queued = False
                    self.emailer.send_attendance([
                        "Travis", "Amory", "Bry"
                    ])
                await asyncio.sleep(500)
            except Exception:
                logger.exception("Failed email error")

    async def loop(self):
        while True:
            try:
                await asyncio.gather(
                    self.read_loop(),
                    self.clear_loop(),
                    self.process_loop(),
                    self.email_loop(),
                )
            except Exception:
                logger.exception("Fatal Error. Restarting...")

    def _clear_message(self):
        self.message = Message.default()

