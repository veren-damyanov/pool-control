"""
Controller processing REST API requests ... TODO: describe briefly

"""
from copy import copy

from sanic.log import logger as log

from poolctl.utils.misc import check_type
from poolctl.model.exc import (
    DeviceNameAlreadyUsed,
    DeviceKindNotRegistered,
    PinAlreadyInUse,
)
from poolctl.model.devices.manager import DeviceManager
from ._common import BaseResource, abort_400, abort_404, abort_409


class DevicesResource(BaseResource):

    def __init__(self, device_manager: DeviceManager):
        check_type(device_manager, DeviceManager)
        self._manager = device_manager

    def get_all(self, payload=None, order_by=None):  # TODO: implement sorting
        return {
            'status': 'success',
            'devices': [device_rec for device_rec in self._manager.get_all()],
        }

    def get(self, name):
        device_rec = self._manager.get_device(name)
        if not device_rec:
            abort_404('gpio device not found for name ' + name)

        return {
            'status': 'success',
            'record': device_rec,
        }

    def post(self, payload):
        device_rec = copy(payload)
        # TODO: check payload payload schema
        name = device_rec['name']
        kind = device_rec['kind']
        gpio = int(device_rec['gpio'])

        try:
            put_record = self._manager.put_device(name, kind, gpio)

        except PinAlreadyInUse as err:
            log.error('Pin already in use by %s (device_rec=%r)', err, device_rec)
            abort_409(f'pin {gpio} already in use')

        except DeviceNameAlreadyUsed:
            log.error('Device name already used: %r (device_rec=%r)', name, device_rec)
            abort_409(f'device with name={name} already exists')

        except DeviceKindNotRegistered as err:
            log.error('Illegal device kind: %r', str(err))
            abort_400(f"illegal device kind {str(err)!r}")

        else:
            return {
                'status': 'success',
                'record': put_record,
            }

    def put(self, payload, name):
        device_rec = copy(payload)
        # TODO: check payload payload schema
        rec_name = str(device_rec['name'])

        if rec_name != name:
            log.error('Put device: bad payload: rec_name=%r != name=%r (device_rec=%r)')
            abort_400(f'body name != url name ({rec_name!r} != {name!r})')

        if not self._manager.has(name):
            log.warning('Put device: device name not found: %r for (device_rec=%r)', name, device_rec)
            abort_404('record not found for name ' + name)

        self._manager.delete_device(name)
        try:
            put_record = self._manager.put_device(name, device_rec['kind'], int(device_rec['gpio']))

        except DeviceKindNotRegistered as err:
            abort_400(f"illegal device kind {str(err)!r}")

        else:
            return {
                'status': 'success',
                'record': put_record,
            }

    def delete(self, name):
        rec = self._manager.delete_device(name)
        if rec is None:
            abort_404(f'record not found for name {name!r}')

        return {
            'status': 'success',
            'deleted_record': rec,
        }

    def get_available_devices(self):
        return {
            'status': 'success',
            'names': self._manager.get_available_names(),
            'gpios': self._manager.get_available_gpios(),
            'kinds': self._manager.get_available_kinds(),
        }

    def get_devices_inuse(self):
        return {
            'status': 'success',
            'names': self._manager.get_devices_inuse(),
        }
