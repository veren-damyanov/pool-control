"""
Singleton instance factories.

"""
from __future__ import annotations

from typing import Dict, Optional
from enum import Enum

from poolctl import settings as cfg
from poolctl.utils.misc import typeof
from poolctl.model.exc import PigpiodNotReachable, PinAlreadyInUse


class PinMode(Enum):
    """Enumeration of GPIO pin modes."""
    INPUT = 0
    OUTPUT = 1
    ALT0 = 4
    ALT1 = 5
    ALT2 = 6
    ALT3 = 7
    ALT4 = 3
    ALT5 = 2


class PinDriverRegistry(object):
    """Registry of PinDriver instances maintaining a map of pin usage state."""

    def __init__(self):
        self._pin_map: Dict[int, Optional[PinDriver]] = dict()

    def close(self):
        [pd.close() for pd in self._pin_map.values() if pd]

    def __del__(self):
        try:
            self.close()
        except Exception as err:
            # TODO: log err before going further
            pass

    def reset(self):
        self.close()
        self._pin_map = dict()

    def ensure_pin_free(self, pin: int):
        old_instance = self._pin_map.get(pin)
        if old_instance:
            raise PinAlreadyInUse(repr(old_instance))

    def register(self, instance: PinDriver):
        pin = instance.pin
        self.ensure_pin_free(pin)
        self._pin_map[pin] = instance

    def deregister_pin(self, pin: int, instance: PinDriver = None):
        old_instance = self._pin_map.get(pin)
        # TODO: check that old_instance is not None
        # TODO: check that old_instance IS instance
        self._pin_map[pin] = None

    def deregister(self, instance: PinDriver):
        pin = instance.pin
        assert pin is not None
        old_instance = self._pin_map.get(pin)
        # TODO: check that old_instance is not None
        # TODO: check that old_instance IS instance
        self._pin_map[pin] = None


_registry = None
_pi_object = None


def get_pin_driver_registry() -> PinDriverRegistry:
    """Return the ``PinDriverRegistry`` single instance."""
    global _registry
    if not _registry:
        _registry = PinDriverRegistry()
    return _registry


def get_pi_instance():  # -> pigpio.pi
    """Return the ``pigpio.pi`` single instance."""
    global _pi_object
    if not _pi_object:
        import pigpio
        _pi_object = pigpio.pi(cfg.PIGPIOD_HOST, cfg.PIGPIOD_PORT)
        if not _pi_object.connected:
            raise PigpiodNotReachable(cfg.PIGPIOD_HOST, cfg.PIGPIOD_PORT)
    return _pi_object


class _PinDriverMeta(type):
    """Simple metaclass allowing early detection of "pin already in use" case."""

    def __call__(cls: PinDriver, pin: int, *args):
        # If pin is already in use - we fail before calling PinDriver.__new__()
        get_pin_driver_registry().ensure_pin_free(pin)
        return super().__call__(pin, *args)


class PinDriver(object, metaclass=_PinDriverMeta):
    """Represent a Raspberry Pi GPIO pin with its Broadcom pin number and mode.
    Maintain a registry of occupied pins and raise exception in case an occupied
    pin is attempted to be re-used again before disposing off the current device.
    """

    def __init__(self, pin: int, mode: PinMode):
        self._pin = pin
        self._mode = mode
        self._pi = get_pi_instance()
        self._pi.set_mode(pin, mode.value)
        get_pin_driver_registry().register(self)

    def on(self):
        """Switch on device connected to this pin on. Default implementation
        does nothing."""

    def off(self):
        """Switch off device connected to this pin on. Default implementation
        does nothing."""

    def _park_pin(self):
        """Set pin into "parked" state, that is, not used."""
        # default safe state is INPUT but it makes more sense
        # to switch off and set to OUTPUT (?)
        self._pi.write(self._pin, 0)
        self._pi.set_mode(self._pin, PinMode.OUTPUT.value)

    def close(self):
        if self._pin is not None:
            self.off()
            self._park_pin()
            get_pin_driver_registry().deregister(self)
            self._pin = None
            self._mode = None

    def __del__(self):
        try:
            self.close()
        except Exception as err:
            # TODO: log err before going further
            pass

    @property
    def pin(self):
        return self._pin

    def __repr__(self):
        return f'<{typeof(self)}(pin={self._pin}, mode={self._mode.name}) object at 0x{id(self):0x}>'
