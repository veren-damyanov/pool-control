"""Unit tests for the devices.gpio module."""

import pytest

from poolctl.model.exc import PinAlreadyInUse
from poolctl.model.devices.base import (
    PinDriver,
    PinMode,
)

from tests._utils.misc import regex
from tests._utils.fixtures.fake_pi import __setup_teardown


def test_create_pin_driver():
    PinDriver(3, PinMode.OUTPUT)


def test_pin_driver__repr__():
    pd_3 = PinDriver(3, PinMode.OUTPUT)
    expected_re = '<PinDriver\(pin=3, mode=OUTPUT\) object at 0x[0-9a-f]+>'
    assert regex(expected_re) == repr(pd_3)


def test_reuse_pin_before_disposal_raises_pinalreadyinuse():
    # reference is important to keep, even if not used, otherwise
    # the pd object is GC-ed promptly ;)
    _ = PinDriver(3, PinMode.OUTPUT)
    with pytest.raises(PinAlreadyInUse):
        PinDriver(3, PinMode.INPUT)
