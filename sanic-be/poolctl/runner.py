"""
TODO:

"""
from __future__ import annotations

from datetime import datetime
from os.path import join as pjoin

from sanic.log import logger as log

from poolctl import settings as cfg
from poolctl.model.devices.manager import DeviceManager
from poolctl.model.scheduler.custom_scheduler import CustomScheduler, PERSIST_STATE_ID, PERSIST_STATE_NAME
from poolctl.model.scheduler.scheduler_store import SchedulerStore
from poolctl.restapi.resources.devices import DevicesResource
from poolctl.restapi.resources.records import RecordsResource


async def persist_state_job(scheduler: CustomScheduler, manager: DeviceManager):
    log.info('Tack! persist_state_job(): time %s  store_id=0x%x, manager_id=0x%x',
              datetime.now(), id(scheduler), id(manager))
    await manager.persist(pjoin(cfg.DATA_PATH, cfg.DEVICES_PERSIST_FILENAME))
    await scheduler.persist(pjoin(cfg.DATA_PATH, cfg.SCHED_PERSIST_FILENAME))


class Runner(object):
    _instance = None

    @classmethod
    def instance(cls, loop=None) -> Runner:
        if not cls._instance:
            assert loop, 'Cannot instantiate GlobalRunner w/o loop'
            cls._instance = Runner(loop)
        return cls._instance

    def __init__(self, loop):
        self.loop = loop
        self.scheduler: CustomScheduler = None
        self.device_manager: DeviceManager = None
        self.schedule_store: SchedulerStore = None
        self.devices_resource: DevicesResource = None
        self.records_resource: RecordsResource = None

    async def launch(self):
        # create essential singletons
        DeviceManager.persistent_file = pjoin(cfg.DATA_PATH, cfg.DEVICES_PERSIST_FILENAME)
        CustomScheduler.persistent_file = pjoin(cfg.DATA_PATH, cfg.SCHED_PERSIST_FILENAME)
        self.device_manager = device_manager = await DeviceManager.from_persistent_data()
        self.scheduler = scheduler = await CustomScheduler.from_persistent_data(event_loop=self.loop)
        self.schedule_store = SchedulerStore.launch(self.scheduler)

        # schedule job for regular persistence
        scheduler.add_job(persist_state_job, 'interval', (scheduler, device_manager),
                          seconds=cfg.PERSIST_STATE_INTERVAL_SEC,
                          id=PERSIST_STATE_ID, name=PERSIST_STATE_NAME)
        scheduler.start()

        # instantiate API resources
        self.devices_resource = DevicesResource(self.device_manager)
        self.records_resource = RecordsResource(self.schedule_store)

        # enable API endpoints
        from poolctl.restapi.endpoints.records import report_records_ep_availability
        from poolctl.restapi.endpoints.devices import report_devices_ep_availability
        from poolctl.restapi.endpoints.logging import report_fe_logging_endpoint_availability
        report_records_ep_availability()
        report_devices_ep_availability()
        report_fe_logging_endpoint_availability()

        # all done
        log.info('Runner launched')

    async def shutdown(self):
        await self.device_manager.persist()
        await self.scheduler.persist()
        self.device_manager.shutdown()
        self.scheduler.shutdown()
        self.schedule_store.shutdown()
        log.info('Runner shut down')
