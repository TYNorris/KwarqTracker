from . import demo_users
from app.src.user.user import User


class StorageHelper:

    def get_user(self, uid: int) -> User:
        return demo_users.get(uid)
