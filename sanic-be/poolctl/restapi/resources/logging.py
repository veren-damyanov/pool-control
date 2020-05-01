"""
Web controller for receiving and processing  front-end logs.
"""
import json
import logging

from sanic.log import logger as server_log
from ._common import BaseResource

# server_log = logging.getLogger(__name__)


class LoggingResource(BaseResource):
    LOGLEVEL_MAP = {
        'trace': logging.DEBUG,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'log': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'exception': logging.ERROR,
    }
    DEFAULT_LOGLEVEL = logging.INFO

    client_log = logging.getLogger('frontend')

    def post(self, request):
        payload = request.json

        try:
            log_level = payload.get('loglevel')
            timestamp = payload['timestamp']
            content = json.dumps(payload['args'])

        except KeyError as err:
            server_log.error("Bad front-end payload=%r (missing key %s)", payload, err)

        else:
            try:
                log_level_code = self.LOGLEVEL_MAP[log_level]
            except KeyError:
                server_log.error("Unrecognized front-end log_level=%r", log_level)
                log_level_code = self.DEFAULT_LOGLEVEL

            self.client_log._log(log_level_code, "(%s) %s", (timestamp, content))

        finally:
            return {'status': 'success'}


frontend_logging_res = LoggingResource()
