import logging
import os

class Config():
    BASE_DIR = os.getcwd()

    LOG_LEVEL = logging.INFO
    LOG_PATH = os.path.join(BASE_DIR, "logs", "app.log")