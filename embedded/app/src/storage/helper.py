
import pyorient

from . import demo_users
from app.src.user.user import User
from app.src.config import get_config

config = get_config()


class StorageHelper:
    client: pyorient.OrientDB
    session_id: object

    def __init__(self):
        self.client = pyorient.OrientDB(config.ORIENT_DB_ADDRESS, 2424)
        self.session_id = self.client.connect(config.ORIENT_DB_LOGIN["user"], config.ORIENT_DB_LOGIN["password"])
        self.client.db_open("Members",
                            config.ORIENT_DB_LOGIN["user"],
                            config.ORIENT_DB_LOGIN["password"],
                            pyorient.DB_TYPE_DOCUMENT)

    def get_user(self, uid: int) -> User:
        response = self.client.query(
            f"SELECT FROM Members "
            f"WHERE uid = {uid}",
            1
        )
        if not response:
            return None

        output = User(**response[0].oRecordData)
        print(output)
        return output
