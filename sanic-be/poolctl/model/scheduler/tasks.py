"""
Scheduler tasks module.

"""
from datetime import datetime
from sanic.log import logger as log


from .record_container import RecordContainer
from ..devices.manager import DeviceManager


def switch_device_on(record_obj: RecordContainer):
    if not record_obj:
        log.error(f'switch_device_on(): empty input: record_obj={record_obj}')
        return
    device = DeviceManager.instance.get_device_driver(record_obj.target)
    device.configure(record_obj.value)
    device.on()
    log.info('Tick! switch_device_on(): %s time %s', record_obj, datetime.now())


def switch_device_off(record_obj: RecordContainer):
    if not record_obj:
        log.error(f'switch_device_off(): empty input: record_obj={record_obj}')
        return
    device = DeviceManager.instance.get_device_driver(record_obj.target)
    device.off()
    log.info('Tick! switch_device_off(): %s time %s', record_obj, datetime.now())
