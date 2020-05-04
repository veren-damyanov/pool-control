"""
/client-logs endpoint

Exposes "POST /client-logs" endpoint for the client app to send logs.
"""
from sanic.log import logger as log
from sanic.response import json

from poolctl.app import app
from poolctl.restapi.resources.logging import frontend_logging_res
from poolctl.restapi.endpoints import API_ROOT

##_ENDPOINT_URL = '/client-logs'

ep_root = API_ROOT + '/client-logs'

def report_fe_logging_endpoint_availability():
    log.info('%s endpoint imported and available', ep_root)


@app.route(ep_root, methods=['POST'])
def do_post(request):
    return json(frontend_logging_res.post(request))
