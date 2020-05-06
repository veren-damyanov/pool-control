"""
Custom logging-related facilities.

"""
import sys
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from poolctl import settings as cfg


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


sanic_root_logger = logging.getLogger('sanic.root')
sanic_root_logger.handlers = []
_handler = RotatingFileHandler(cfg.LOG_FILE_PATH, maxBytes=2097152, backupCount=5, encoding='utf-8')
_handler.setFormatter(logging.Formatter(cfg.LOG_FILE_FORMAT))
_handler.setLevel(cfg.LOG_FILE_LEVEL)
sanic_root_logger.addHandler(_handler)
_handler = StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter(cfg.LOG_CONSOLE_FORMAT))
_handler.setLevel(cfg.LOG_CONSOLE_LEVEL)
sanic_root_logger.addHandler(_handler)
sanic_root_logger.addFilter(CorsFilter())  # get rid of CORS: messages for now  # TODO: revisit

sanic_access_logger = logging.getLogger('sanic.access')
sanic_access_logger.handlers = []
_handler = RotatingFileHandler(cfg.LOG_ACCESS_FILE_PATH, maxBytes=2097152, backupCount=5, encoding='utf-8')
_handler.setFormatter(logging.Formatter(cfg.LOG_ACCESS_FILE_FORMAT))
_handler.setLevel(cfg.LOG_ACCESS_FILE_LEVEL)
sanic_access_logger.addHandler(_handler)


# sanic_root_logger.addFilter(LevelFilter(cfg.LOG_ACCESS_FILE_LEVEL))  # decrease verbosity for now  # TODO: revisit

def announce_logging_availability():
    sanic_root_logger.warning('Sanic root logger activated')
    sanic_access_logger.warning('Sanic access logger activated')
