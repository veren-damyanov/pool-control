"""
Default settings for the Pool Control application.

Other settings files would typically import this one first and then
overwrite those values needed a re-definition.

"""
from ._gpio_data import GPIO_TABLE as _GPIO_TABLE

GPIO_TABLE = _GPIO_TABLE

PIGPIOD_HOST = 'localhost'
PIGPIOD_PORT = 8888

ALL_DEVICE_NAMES = (
    'P1', 'P2', 'L1', 'L2', 'L3', 'L4',  # 'T',  # currently no support for 'T'
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
)

APP_ARGS = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False,
}

# Logging related settings

LOG_CONSOLE_FORMAT = '%(levelname)s: %(message)s'
LOG_FILE_FORMAT = '%(asctime)s [%(levelname)-7s] %(name)s - %(message)s'
LOG_ACCESS_FILE_FORMAT = LOG_FILE_FORMAT

LOG_FILE_PATH = '/var/log/poolctl/sanic-app.log'
LOG_ACCESS_FILE_PATH = '/var/log/poolctl/sanic-access.log'

LOG_CONSOLE_LEVEL = 'INFO'
LOG_FILE_LEVEL = 'DEBUG'
LOG_ACCESS_FILE_LEVEL = 'INFO'
