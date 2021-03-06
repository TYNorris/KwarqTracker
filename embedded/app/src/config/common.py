import logging
import os

from .secrets import db_password, email_password

class Config():
    BASE_DIR = os.getcwd()

    LOG_LEVEL = logging.DEBUG
    LOG_PATH = os.path.join(BASE_DIR, "logs", "app.log")

    ORIENT_DB_ADDRESS = "localhost"
    ORIENT_DB_LOGIN = {
        "user": "root",
        "password": db_password
    }

    DESTINATION_ADDRESSES = [
        "travis@team2423.org"
    ]
    EMAIL_ADDRESS = "attendance@team2423.org"
    EMAIL_PASSWORD = email_password
