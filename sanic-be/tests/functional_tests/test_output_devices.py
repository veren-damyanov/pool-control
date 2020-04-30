"""Live GPIO drivers test"""

from typing import List
import time

import pytest

from poolctl.model.devices.base import (
    get_pin_driver_registry,
)
from poolctl.model.devices.named import (
    InputDeviceDriver,
    OutputDeviceDriver,
    PwmDeviceDriver,
    LightDriver,
    PumpDriver,
)


@pytest.fixture(autouse=True)
def __setup_teardown():
    yield __setup()
    __teardown()


def __setup():
    return None


def __teardown():
    get_pin_driver_registry().reset()


def test_on_off():
    in1 = InputDeviceDriver(9, 'X1')  # not yet implemented
    d1 = OutputDeviceDriver(3, 'D1')
    l1 = LightDriver(15, 'L1', 100)
    l2 = LightDriver(27, 'L2', 100)
    p1 = PumpDriver(10, 'P1', 100)
    p2 = PumpDriver(7, 'P2', 100)
    _all = [in1, d1, l1, l2, p1, p2]
    for dev in _all:  dev.on()
    time.sleep(0.5)
    for dev in _all:  dev.off()


def test_pwm_grades():
    l0 = LightDriver(3, 'L0', 2)
    l1 = LightDriver(15, 'L1', 2)
    l2 = LightDriver(27, 'L2', 2)
    p1 = PumpDriver(10, 'P1', 2)
    p2 = PumpDriver(7, 'P2', 2)
    _all: List[PwmDeviceDriver] = [l0, l1, l2, p1, p2]
    levels = (1, 3, 6, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 100)
    for dev in _all:  dev.on()
    for level in levels:
        time.sleep(0.05)
        for dev in _all:  dev.set_duty_cycle(level)
    for level in reversed(levels):
        time.sleep(0.1)
        for dev in _all:  dev.set_duty_cycle(level)
