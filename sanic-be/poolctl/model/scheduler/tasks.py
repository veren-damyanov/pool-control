"""
Scheduler tasks module.

"""
from datetime import datetime

from sanic.log import logger as log

from poolctl.model.devices.manager import DeviceManager
from poolctl.model.scheduler.record_container import RecordContainer


def switch_device_on(device_manager: DeviceManager, record_obj: RecordContainer):
    if not (device_manager and record_obj):
        log.error(f'switch_device_on(): empty input: device_manager={device_manager} record_obj={record_obj}')
        return
    device = device_manager.get_device_driver(record_obj.target)
    device.configure(record_obj.value)
    device.on()
    log.info('Tick! switch_device_on(): %s time %s', record_obj, datetime.now())


def switch_device_off(device_manager: DeviceManager, record_obj: RecordContainer):
    if not (device_manager and record_obj):
        log.error(f'switch_device_off(): empty input: device_manager={device_manager} record_obj={record_obj}')
        return
    device = device_manager.get_device_driver(record_obj.target)
    device.off()
    log.info('Tick! switch_device_off(): %s time %s', record_obj, datetime.now())
