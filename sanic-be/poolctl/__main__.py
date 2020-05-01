"""Run the poolctl back-end."""

import sys
import logging

from sanic.log import logger as log


def main():
    try:
        from poolctl import settings as cfg
        from poolctl.app import app
        app.run(**cfg.APP_ARGS)

    except KeyboardInterrupt:
        log.info('\n** Canceled by user')
        return 0

    except Exception as err:
        from poolctl.utils.misc import typeof
        message = f'UNHANDLED ERROR: {typeof(err)}: {err}'
        print(message, file=sys.stderr)
        logging.getLogger().error(message, exc_info=True)
        return 3

    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())
