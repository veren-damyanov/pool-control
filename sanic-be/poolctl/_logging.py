"""
Custom logging-related facilities.

"""
import logging


class CorsFilter(logging.Filter):
    """Suppress CORS log messages below given level."""

    def __init__(self, levelno: int = logging.INFO):
        super().__init__()
        self._levelno = levelno

    def filter(self, record):
        return not (record.levelno < self._levelno and record.msg.startswith('CORS:'))


class LevelFilter(logging.Filter):

    def __init__(self, levelno: int = logging.INFO):
        super().__init__()
        self._levelno = levelno

    def filter(self, record):
        return record.levelno >= self._levelno
