"""
TODO:

"""
from __future__ import annotations

from typing import Optional, Dict, List

from sanic.log import logger as log

from poolctl import settings as cfg
from poolctl.utils.misc import nameof
from poolctl.model.mixins import PersistMixin
from poolctl.model.devices.named import DeviceDriver, get_device_names_registry


class DeviceManager(PersistMixin, object):

    @classmethod
    async def _from_persistent_data(cls, data: Optional[dict], **kw) -> DeviceManager:
        manager = DeviceManager()
        if data:
            for rec in data.values():
                manager.put_device(**rec)
        manager.set_clean()
        return manager

    def __init__(self):
        PersistMixin.__init__(self)
        self.ALL_GPIOS = tuple(sorted(elem[1] for elem in cfg.GPIO_TABLE))
        self.devices: Dict[str, DeviceDriver] = dict()

    def _persistent_data(self):
        result = dict()
        for device in self.devices.values():
            result[device.name] = dict(name=device.name, kind=device.__kind__, pin=device.pin)
        return result

    def shutdown(self):
        for dev in self.devices.values():
            dev.close()

    def has(self, name: str):
        return name in self.devices

    def put_device(self, name: str, kind: str, pin: int):
        # What changes within the device setup? Can we do that if there are records using
        # this device in the scheduler?
        # FIXME: discuss above issues and adopt the code to handle all that correctly.
        name, kind, pin = str(name), str(kind), int(pin)
        DeviceKlass = get_device_names_registry().klass_for(kind)
        device: DeviceDriver = DeviceKlass(pin, name)
        self.devices[name] = device
        self.set_dirty()
        log.info('Created device name=%r: kind=%r pin=%r klass=%r', name, kind, pin, nameof(DeviceKlass))
        return device.as_dict()

    def get_device_driver(self, name: str) -> Optional[DeviceDriver]:
        try:
            return self.devices[name]
        except KeyError:
            log.warning('Getting device: NOT found for name=%r', name)
            return None

    def get_device(self, name: str) -> Optional[dict]:
        device = self.get_device_driver(name)
        return device.as_dict() if device else None

    def delete_device(self, name: str) -> Optional[dict]:
        # FIXME: We need to check if there's something for this device in the scheduler
        try:
            device = self.devices[name]
            self.set_dirty()
        except KeyError:
            log.warning('Deleting device failed: name=%r not found', name)
            return None

        result = device.as_dict()
        device.close()
        del self.devices[name]
        log.warning('Deleted device for name=%r', name)
        return result

    def get_all(self) -> List[dict]:
        return [device.as_dict() for device in self.devices.values()]

    @staticmethod
    def get_all_names():
        return list(cfg.ALL_DEVICE_NAMES)

    def get_available_names(self):
        return [name for name in cfg.ALL_DEVICE_NAMES if name not in self.devices]

    def get_available_gpios(self):
        used_pins = set(device.pin for device in self.devices.values())
        return [pin for pin in self.ALL_GPIOS if pin not in used_pins]

    def get_available_kinds(self):
        return sorted(get_device_names_registry().all_kinds().keys())

    def get_devices_inuse(self):
        return [name for name in cfg.ALL_DEVICE_NAMES if name in self.devices]
