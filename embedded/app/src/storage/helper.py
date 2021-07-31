import logging
import pyorient

from . import demo_users
from app.src.user.user import User
from app.src.config import get_config

config = get_config()
logger = logging.getLogger(__name__)


class StorageHelper:
    client: pyorient.OrientDB
    session_id: object

    def __init__(self):
        self.client = pyorient.OrientDB(config.ORIENT_DB_ADDRESS, 2424)
        self.session_id = self.client.connect(config.ORIENT_DB_LOGIN["user"], config.ORIENT_DB_LOGIN["password"])
        self._clusters = self.client.db_open("Members",
                            config.ORIENT_DB_LOGIN["user"],
                            config.ORIENT_DB_LOGIN["password"],
                            pyorient.DB_TYPE_DOCUMENT)

    def get_user(self, uid: int) -> User:
        response = self._query_user(uid)
        if not response:
            return None

        output = User(**response[0].oRecordData)
        return output

    def add_user(self, user: User) -> bool:
        try:
            record = self._format_user(user)
            cluster = next(filter(lambda c: c.name is not None and 'member' in str(c.name), self._clusters))
            rec_position = self.client.record_create(cluster.id, record)
            return True
        except Exception:
            logger.exception(f"Failed to add new user: {user}")
        return False

    def update_user(self, user: User) -> bool:
        try:
            current = self._query_user(user.uid)
            if current is None:
                logger.error(f"Could not update user. No user with ID {user.uid}")
                return False
            record = current[0]
            self.client.record_update(record._rid, record._rid, self._format_user(user), record._version)
            return True
        except Exception:
            logger.exception(f"Failed to update user: {user}")
        return False

    def _query_user(self, uid: int):
        return self.client.query(
            f"SELECT FROM Members "
            f"WHERE uid = {uid}",
            1
        )

    @staticmethod
    def _format_user(user: User) -> dict:
        return {'@Members': user.serialize()}
