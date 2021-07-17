import logging

from .common import Config

class DevConfig(Config):
    LOG_LEVEL = logging.DEBUG