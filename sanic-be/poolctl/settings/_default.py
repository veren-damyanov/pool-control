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
    'P1', 'P2', 'L1', 'L2', 'L3', 'L4', 'T',
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9',
)

APP_ARGS = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': False,
}
