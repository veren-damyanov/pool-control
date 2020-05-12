"""
TODO:

"""
from __future__ import annotations

from datetime import datetime, timedelta
from os.path import join as pjoin

from apscheduler.jobstores.base import ConflictingIdError
from sanic.log import logger as log

from poolctl import settings as cfg
from poolctl.model import PERSIST_DEVICES_JOB_ID, PERSIST_SCHEDULE_JOB_ID
from poolctl.model.mixins import DirtyListenerT, PersistMixin
from poolctl.model.devices.manager import DeviceManager
from poolctl.model.scheduler.custom_scheduler import CustomScheduler
from poolctl.model.scheduler.scheduler_store import SchedulerStore
from poolctl.restapi.resources.devices import DevicesResource
from poolctl.restapi.resources.records import RecordsResource


async def persist_state_job(persist_obect: PersistMixin):
    log.info('Tack! persist_state_job(): time %s  id(persist_obect)=0x%x', datetime.now(), id(persist_obect))
    await persist_obect.persist()
    # await manager.persist(pjoin(cfg.DATA_PATH, cfg.DEVICES_PERSIST_FILENAME))
    # await scheduler.persist(pjoin(cfg.DATA_PATH, cfg.SCHED_PERSIST_FILENAME))


class Runner(DirtyListenerT, object):
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

    CLASS_TO_JOB_ID_MAP = {
        CustomScheduler: PERSIST_SCHEDULE_JOB_ID,
        DeviceManager: PERSIST_DEVICES_JOB_ID,
    }

    def on_dirty(self, dirty_object: PersistMixin):
        # schedule job for regular persistence
        job_id = self.CLASS_TO_JOB_ID_MAP[type(dirty_object)]
        run_date = datetime.now() + timedelta(seconds=cfg.PERSIST_STATE_OFFSET_SEC)
        try:
            self.scheduler.add_job(persist_state_job, 'date', (dirty_object,), run_date=run_date,
                                   id=job_id, name=job_id)
        except ConflictingIdError as err:
            log.info('Job with id %r already scheduled. Skipping.', job_id)
        else:
            log.info('Job with id %r scheduled.', job_id)

    async def launch(self):
        # create essential singletons
        DeviceManager.persistent_file = pjoin(cfg.DATA_PATH, cfg.DEVICES_PERSIST_FILENAME)
        CustomScheduler.persistent_file = pjoin(cfg.DATA_PATH, cfg.SCHED_PERSIST_FILENAME)
        self.device_manager = device_manager = await DeviceManager.from_persistent_data()
        self.device_manager.dirty_listener = self
        self.scheduler = scheduler = await CustomScheduler.from_persistent_data(event_loop=self.loop)
        self.scheduler.dirty_listener = self
        self.schedule_store = SchedulerStore.launch(self.scheduler)
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
