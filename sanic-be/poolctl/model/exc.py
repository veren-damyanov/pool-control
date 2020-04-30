"""
Exception classes for the Pool Control app model.
"""


class PoolCtlDeviceError(Exception):
    """Base class for any Pool Control device specific errors."""


class NamedDevicesRegistryError(PoolCtlDeviceError):
    """Base class for named devices registry specific errors."""


class UnknownDeviceKind(NamedDevicesRegistryError):
    """Raise when unknown string name of device kind is used to query
    the ``_CustomDevTypeRegistry``."""


class DeviceNameAlreadyUsed(NamedDevicesRegistryError):
    """Raise on an attempt to create a device with the same name as of
    other existing device."""


class DeviceKindAlreadyRegistered(NamedDevicesRegistryError):
    """Raise on an attempt to register an already registered device kind.
    Device kinds are declared via ``__kind__`` property to DeviceDriver
    subclasses, thus getting this is probably caused by two DeviceDriver
    subclasses having the same __kind__."""


class DeviceKindNotRegistered(NamedDevicesRegistryError):
    """Raise when a DeviceDriver subclass expected to be in the
    DeviceNamesRegistry is not there."""


class RegisteredInstanceMismatch(NamedDevicesRegistryError):
    """Raise on failure to match registered instance with another instance
    having same identification."""


class GpioDeviceError(PoolCtlDeviceError):
    """Base class for GPIO device specific errors."""


class IllegalPinNumber(GpioDeviceError):
    """Raise when incorrect GPIO PIN number is used."""


class PinAlreadyInUse(GpioDeviceError):
    """Raise on an attempt to create new GpioDevice object for a _pin
    number that has already been assigned to another GpioDevice object
    and not released."""


class DutyCycleNotSet(GpioDeviceError):
    """Raise when PwmDevice::on() is called but no proper duty cycle
    is set."""


class PigpiodNotReachable(PoolCtlDeviceError):
    """Raise when there are issues connected to the Pi pigpio."""
