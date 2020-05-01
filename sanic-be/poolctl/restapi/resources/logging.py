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

    client_log = server_log.getChild('frontend')

    def post(self, request):

        payload = request.json

        try:
            log_level = payload.get('loglevel')
            timestamp = payload['timestamp']
            msg_payload = payload['args']
            if isinstance(msg_payload, list):
                logline = '|'.join(map(str, msg_payload))
            else:
                logline = json.dumps(payload)

        except KeyError as err:
            server_log.error("Bad front-end payload=%r (missing key %s)", payload, err)

        else:
            try:
                log_level_code = self.LOGLEVEL_MAP[log_level]
            except KeyError:
                server_log.error("Unrecognized front-end log_level=%r", log_level)
                log_level_code = self.DEFAULT_LOGLEVEL

            self.client_log.log(log_level_code, "FRONT: (%s) %s", timestamp, logline)

        finally:
            return {'status': 'success'}


frontend_logging_res = LoggingResource()
