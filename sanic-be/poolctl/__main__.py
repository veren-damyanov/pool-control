"""Run the poolctl back-end."""

import sys
import logging

from sanic.log import logger as log

from poolctl import settings as cfg
from poolctl.utils.misc import typeof
from poolctl.app import app


@app.listener('before_server_start')
async def initialize_scheduler(app, loop):
    log.info('Server starting up...')
    from poolctl.restapi.endpoints.devices import report_devices_ep_availability
    report_devices_ep_availability()


@app.listener('before_server_stop')
async def async_notify_server_stopping(app, loop):
    log.info('Back-end shutting down...')


@app.listener('after_server_stop')
async def async_notify_server_stopping(app, loop):
    log.info('Back-end shut down cleanly.')


def main():
    try:
        app.run(**cfg.APP_ARGS)

    except KeyboardInterrupt:
        log.info('\n** Canceled by user')
        return 0

    except Exception as err:
        logging.getLogger().error(
            'UNHANDLED ERROR: %s: %s', typeof(err), err, exc_info=True)
        return 3

    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
