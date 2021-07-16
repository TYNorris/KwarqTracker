from config import get_config
from logger.logger import setup_logger

config = get_config()

if __name__ == '__main__':
    setup_logger()