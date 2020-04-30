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
    print(f'Tick! switch_device_on({record_obj}): time {datetime.now()}')


def switch_device_off(device_manager: DeviceManager, record_obj: RecordContainer):
    if not (device_manager and record_obj):
        log.error(f'switch_device_off(): empty input: device_manager={device_manager} record_obj={record_obj}')
        return
    device = device_manager.get_device_driver(record_obj.target)
    device.off()
    print(f'Tick! switch_device_off({record_obj}): time {datetime.now()}')
