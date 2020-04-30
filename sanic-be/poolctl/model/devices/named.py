"""
TODO: document

"""
from __future__ import annotations

from typing import Type, Optional, Dict

from poolctl.utils.misc import typeof, nameof
from poolctl.model.exc import (
    DeviceNameAlreadyUsed,
    RegisteredInstanceMismatch,
    DeviceKindAlreadyRegistered,
    DeviceKindNotRegistered,
)
from poolctl.model.devices.base import PinMode, PinDriver, _PinDriverMeta


class DeviceNamesRegistry(object):

    def __init__(self):
        self._names: Dict[str, DeviceDriver] = dict()
        self._kinds: Dict[str, Type[DeviceDriver]] = dict()

    def ensure_name_not_used(self, name: str):
        old_instance = self._names.get(name)
        if old_instance:
            raise DeviceNameAlreadyUsed(repr(old_instance))

    def ensure_name_used_by(self, name: str, instance: DeviceDriver):
        old_instance = self._names.get(name)
        if not old_instance:
            raise RegisteredInstanceMismatch(f'name {name!r} not found in name registry')
        if instance is not old_instance:
            raise RegisteredInstanceMismatch(f'expected {old_instance!r} but was {instance!r} for name {name}')

    def ensure_kind_not_used(self, kind: str):
        old_klass = self._names.get(kind)
        if old_klass:
            raise DeviceKindAlreadyRegistered(nameof(old_klass))

    def register_kind(self, kind: str, klass: Type[DeviceDriver]):
        self.ensure_kind_not_used(kind)
        self._kinds[kind] = klass

    def all_kinds(self) -> Dict[str, Type[DeviceDriver]]:
        return self._kinds.copy()

    def klass_for(self, kind: str) -> Type[DeviceDriver]:
        try:
            return self._kinds[kind]
        except KeyError:
            raise DeviceKindNotRegistered(kind)

    def register_name(self, instance: DeviceDriver):
        name = instance.name
        self.ensure_name_not_used(name)
        self._names[name] = instance

    def deregister_name(self, instance: DeviceDriver):
        name = instance.name
        self.ensure_name_used_by(name, instance)
        del self._names[name]


_names_registry = None


def get_device_names_registry():
    global _names_registry
    if not _names_registry:
        _names_registry = DeviceNamesRegistry()
    return _names_registry


class _DeviceDriverMeta(_PinDriverMeta):
    """Metaclass allowing early detection of "name already used" case."""

    def __init__(cls: Type[DeviceDriver], name: str, bases: tuple, attribs: dict):
        kind = attribs['__kind__']
        get_device_names_registry().register_kind(kind, cls)
        super().__init__(name, bases, attribs)

    def __call__(cls: DeviceDriver, pin: int, *args):
        # If name already used - we fail before calling DeviceDriver.__new__()
        # args is either (mode: PinMode, name: str) or just (name: str,)
        name = args[1] if isinstance(args[0], PinMode) else args[0]
        get_device_names_registry().ensure_name_not_used(name)
        return super().__call__(pin, *args)


class DeviceDriver(PinDriver, metaclass=_DeviceDriverMeta):
    __kind__ = None

    def __init__(self, pin: int, mode: PinMode, name: str):
        super().__init__(pin, mode)
        self._name: str = name
        get_device_names_registry().register_name(self)

    def close(self):
        super().close()
        if self._name:
            get_device_names_registry().deregister_name(self)
            self._name = None

    def __repr__(self):
        return f'<{typeof(self)}(pin={self._pin}, mode={self._mode.name}, name={self._name!r})' \
               f' object at 0x{id(self):0x}>'

    @property
    def name(self):
        return self._name

    def as_dict(self):
        return dict(
            name=self._name,
            kind=self.__kind__,
            gpio=self._pin,
        )


class InputDeviceDriver(DeviceDriver):
    __kind__ = None

    def __init__(self, pin: int, name: str):
        super().__init__(pin, PinMode.INPUT, name)


class OutputDeviceDriver(DeviceDriver):
    __kind__ = None

    def __init__(self, pin: int, name: str):
        super().__init__(pin, PinMode.OUTPUT, name)
        self._is_on = None  # "declare"
        self.off()

    def on(self):
        self._pi.write(self._pin, 1)
        self._is_on = True

    def off(self):
        self._pi.write(self._pin, 0)
        self._is_on = False


class PwmDeviceDriver(OutputDeviceDriver):
    __kind__ = None

    def __init__(self, pin, name, duty_cycle=0):
        super().__init__(pin, name)
        self._duty_cycle = duty_cycle  # percent

    def _apply_duty_cycle(self):
        value = round(255.0 * float(self._duty_cycle) / 100.0)
        self._pi.set_PWM_dutycycle(self._pin, value)

    def set_duty_cycle(self, duty_cycle):
        self._duty_cycle = duty_cycle  # percent
        if self._is_on:
            self._apply_duty_cycle()

    def on(self):
        self._is_on = True
        self._apply_duty_cycle()

    def off(self):
        self._pi.set_PWM_dutycycle(self._pin, 0)
        self._is_on = False


class PumpDriver(PwmDeviceDriver):
    __kind__ = 'pump'


class LightDriver(PwmDeviceDriver):
    __kind__ = 'light'


class DigitalRelay(OutputDeviceDriver):
    __kind__ = 'relay'
