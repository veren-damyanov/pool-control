"""Run the poolctl back-end."""

import sys
import logging

from sanic.log import logger as log

from poolctl import settings as cfg
from poolctl.utils.misc import typeof
from poolctl.app import app


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
