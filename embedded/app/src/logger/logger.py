import logging

from logging.handlers import TimedRotatingFileHandler

from ..config import get_config

config = get_config()


def setup_logger():
    handler = TimedRotatingFileHandler(
        filename=config.LOG_PATH,
        backupCount=30,
        when='MIDNIGHT'
    )

    handler.setLevel(config.LOG_LEVEL)
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    )

    dash_logger = logging.getLogger('werkzeug')
    dash_logger.setLevel(logging.WARNING)

    root = logging.getLogger()
    root.setLevel(config.LOG_LEVEL)
    root.addHandler(handler)
