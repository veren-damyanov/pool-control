"""
Custom logging-related facilities.

"""
import logging


class CorsFilter(logging.Filter):
    """Suppress CORS log messages below given level."""

    def __init__(self, levelno: int = logging.INFO):
        super(CorsFilter, self).__init__()
        self._levelno = levelno

    def filter(self, record):
        return not (record.levelno < self._levelno and record.msg.startswith('CORS:'))