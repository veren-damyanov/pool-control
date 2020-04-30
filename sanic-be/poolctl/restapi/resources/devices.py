"""
Controller processing REST API requests ... TODO: describe briefly

"""
from sanic.log import logger as log

from poolctl.utils.misc import Undef, check_type
from poolctl.model.exc import DeviceNameAlreadyUsed, DeviceKindNotRegistered, PinAlreadyInUse
from poolctl.model.devices.manager import DeviceManager
from ._common import BaseResource, abort_400, abort_404, abort_409

_devices_resource = None


def devices_resource():
    global _devices_resource
    if not _devices_resource:
        _devices_resource = DevicesResource(DeviceManager())
    return _devices_resource


class DevicesResource(BaseResource):

    def __init__(self, device_manager: DeviceManager):
        check_type(device_manager, DeviceManager)
        self._devmgr = device_manager

    def get_all(self, order_by=None):  # TODO: implement sorting
        return {
            'status': 'success',
            'devices': [device_rec for device_rec in self._devmgr.get_all()],
        }

    def get(self, request, name):
        device_rec = self._devmgr.get_device(name)
        if not device_rec:
            abort_404('gpio device not found for name ' + name)

        return {
            'status': 'success',
            'record': device_rec,
        }

    def post(self, request):
        device_rec = request.json
        # TODO: check request payload schema
        name = device_rec['name']
        kind = device_rec['kind']
        gpio = int(device_rec['gpio'])

        try:
            put_record = self._devmgr.put_device(name, kind, gpio)

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

    def put(self, request, name):
        device_rec = request.json
        # TODO: check request payload schema
        rec_name = str(device_rec['name'])

        if rec_name != name:
            log.error('Put device: bad request: rec_name=%r != name=%r (device_rec=%r)')
            abort_400(f'body name != url name ({rec_name!r} != {name!r})')

        if not self._devmgr.has(name):
            log.warning('Put device: device name not found: %r for (device_rec=%r)', name, device_rec)
            abort_404('record not found for name ' + name)

        self._devmgr.delete_device(name)
        try:
            put_record = self._devmgr.put_device(name, device_rec['kind'], int(device_rec['gpio']))

        except DeviceKindNotRegistered as err:
            abort_400(f"illegal device kind {str(err)!r}")

        else:
            return {
                'status': 'success',
                'record': put_record,
            }

    def delete(self, request, name):
        rec = self._devmgr.delete_device(name)
        if rec is None:
            abort_404(f'record not found for name {name!r}')

        return {
            'status': 'success',
            'deleted_record': rec,
        }

    def get_available_devices(self, request):
        return {
            'status': 'success',
            'names': self._devmgr.get_available_names(),
            'gpios': self._devmgr.get_available_gpios(),
        }

    def get_devices_inuse(self, request):
        return {
            'status': 'success',
            'names': self._devmgr.get_devices_inuse(),
        }
