import logging

from config import get_config
from logging.handlers import TimedRotatingFileHandler

config = get_config()

def setup_logger():
    logger = TimedRotatingFileHandler(
        filename= config.LOG_PATH,
        backupCount= 30,
        when= 'MIDNIGHT'
    )

    logger.setLevel(config.LOG_LEVEL)
    logger.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    )
    