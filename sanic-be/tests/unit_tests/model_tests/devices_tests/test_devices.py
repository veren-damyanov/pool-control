"""Unit tests for the devices module."""

import pytest

from poolctl.model.exc import PinAlreadyInUse
from poolctl.model.devices.base import PinMode
from poolctl.model.devices.named import (
    DeviceDriver,
    InputDeviceDriver,
    OutputDeviceDriver,
    PwmDeviceDriver,
)

from tests._utils.fixtures.fake_pi import __setup_teardown


def test_devicedriver():
    DeviceDriver(3, PinMode.OUTPUT, 'L1')


def test_inputdevicedriver():
    InputDeviceDriver(9, 'X1')


def test_outputdevicedriver():
    OutputDeviceDriver(3, 'L1')


def test_pwmdevicedriver():
    PwmDeviceDriver(3, 'L1', 75)


def test_using_same_pin_again_raises_pinalreadyinuse():
    _ = DeviceDriver(9, PinMode.OUTPUT, 'L1')  # keep the reference
    with pytest.raises(PinAlreadyInUse):
        OutputDeviceDriver(9, 'L2')
    with pytest.raises(PinAlreadyInUse):
        PwmDeviceDriver(9, 'L3', 75)


def test_using_same_name_again_raises_WHAT():
    _ = DeviceDriver(9, PinMode.OUTPUT, 'L1')  # keep the reference
    DeviceDriver(11, PinMode.INPUT, 'B2')
