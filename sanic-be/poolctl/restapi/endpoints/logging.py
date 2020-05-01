"""
/client-logs endpoint

Exposes "POST /client-logs" endpoint for the client app to send logs.
"""

from sanic.response import json

from poolctl.app import app
from poolctl.restapi.resources.logging import frontend_logging_res

_ENDPOINT_URL = '/client-logs'


def report_fe_logging_endpoint_availability():
    print(_ENDPOINT_URL + ' endpoint imported and available')


@app.route(_ENDPOINT_URL, methods=['POST'])
def do_post(request):
    return json(frontend_logging_res.post(request))
