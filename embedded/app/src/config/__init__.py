import platform

from .common import Config
from .dev import DevConfig

def get_config() -> Config:
    if platform.system() == 'Windows':
        return DevConfig()
    return Config()
