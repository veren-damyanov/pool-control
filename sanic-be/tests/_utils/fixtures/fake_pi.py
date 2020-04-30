"""
A fixture suitable for unit tests involving GPIO-enabled classes.

It mocks the pigpio pi object and resets the driver registry for each test
to ensure proper isolation.

"""
import pytest

from poolctl.model.devices.base import get_pin_driver_registry


@pytest.fixture(autouse=True)
def __setup_teardown(mocker):
    yield __setup(mocker)
    __teardown()


def __setup(mocker):
    mocker.patch('poolctl.model.devices.base.get_pi_instance')
    return None


def __teardown():
    get_pin_driver_registry().reset()
