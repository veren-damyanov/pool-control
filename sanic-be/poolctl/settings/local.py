"""
Local environment settings.

See __init__ docstring for environment setup details.

"""

#: Bind to all interfaces to ease testing both locally and by someone sitting next
APP_ARGS = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': True,
}

LOG_CONSOLE_FORMAT = '%(asctime)s [%(levelname)-7s] %(name)s - %(message)s'
LOG_FILE_FORMAT = '%(asctime)s [%(levelname)-7s] %(name)s - %(message)s'
LOG_ACCESS_FILE_FORMAT = LOG_FILE_FORMAT

LOG_FILE_PATH = '/tmp/sanic-app.log'
LOG_ACCESS_FILE_PATH = '/tmp/sanic-access.log'

LOG_CONSOLE_LEVEL = 'DEBUG'
LOG_FILE_LEVEL = 'DEBUG'
LOG_ACCESS_FILE_LEVEL = 'INFO'

DATA_PATH = '/tmp'
PERSIST_STATE_INTERVAL_SEC = 60
