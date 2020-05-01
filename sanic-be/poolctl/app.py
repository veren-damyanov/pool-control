"""
Sanic application execution module.

"""
import logging

from sanic.log import logger as log
from sanic.exceptions import NotFound
from sanic.response import json
from sanic_cors import CORS
from sanic import Sanic
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from poolctl.utils.async_stuff import all_tasks_to_close
from poolctl.model.devices.manager import DeviceManager
from poolctl.model.scheduler.scheduler_store import SchedulerStore
from poolctl.restapi.resources.devices import DevicesResource
from poolctl.restapi.resources.records import RecordsResource
from poolctl._logging import CorsFilter

logging.getLogger('sanic.root').addFilter(CorsFilter())


def create_app() -> Sanic:
    app = Sanic('poolctl-be', load_env=False)
    CORS(app)  # TODO: Revisit security
    return app


app = create_app()


@app.exception(NotFound)
def handle_404(request, exc):
    log.warning('Not Found (404): %s', exc)
    return json({
        'status': 'error',
        'message': str(exc),
    }, status=404)


@app.listener('before_server_start')
async def initialize_scheduler(app, loop):
    log.info('Server starting up...')
    app.runner = Runner.instance(loop)
    app.runner.launch()
    from poolctl.restapi.endpoints.records import report_records_ep_availability
    from poolctl.restapi.endpoints.devices import report_devices_ep_availability
    from poolctl.restapi.endpoints.logging import report_fe_logging_endpoint_availability
    report_records_ep_availability()
    report_devices_ep_availability()
    report_fe_logging_endpoint_availability()


@app.listener('after_server_stop')
async def async_notify_server_stopping(app, loop):
    log.info('Back-end shutting down...')
    app.runner.shutdown()
    await all_tasks_to_close()
    log.info('Back-end shut down cleanly.')


class Runner(object):
    _instance = None

    @classmethod
    def instance(cls, loop=None):
        if not cls._instance:
            assert loop, 'Cannot instantiate GlobalRunner w/o loop'
            cls._instance = Runner(loop)
        return cls._instance

    def __init__(self, loop):
        self.loop = loop
        self.sched_store = None
        self.records_resource = None
        self.devices_resource = None

    def launch(self):
        scheduler = AsyncIOScheduler({'event_loop': self.loop})
        device_manager = DeviceManager()
        sched_store = SchedulerStore.launch(scheduler, device_manager)
        self.records_resource = RecordsResource(sched_store)
        self.devices_resource = DevicesResource(device_manager)
        self.sched_store = sched_store
        log.info('Runner launched')

    def shutdown(self):
        self.sched_store.shutdown()
