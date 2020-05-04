"""
/devices endpoint implementation.

TODO: describe briefly

"""
from functools import lru_cache

from sanic.log import logger as log
from sanic.response import json

from poolctl.app import app, Runner
from poolctl.model.devices.manager import DeviceManager
from poolctl.restapi.endpoints import API_ROOT


ep_root = API_ROOT + '/devices'


@lru_cache(maxsize=1)
def devices_resource():
    DeviceManager()
    return Runner.instance().devices_resource


def report_devices_ep_availability():
    log.info(ep_root + ' endpoint imported and available')


@app.route(ep_root, methods=('GET', 'POST', 'OPTIONS'))
def get_all_or_create(request):
    method = request.method.upper()
    func_map = {
        'GET': devices_resource().get_all,
        'POST': devices_resource().post,
    }
    return json(func_map[method](request))


@app.route(ep_root + '/<name:string>', methods=('GET',))
def get_one(request, name):
    return json(devices_resource().get(request, name))


@app.route(ep_root + '/<name:string>', methods=('PUT',))
def put_one(request, name):
    return json(devices_resource().put(request, name))


@app.route(ep_root + '/<name:string>', methods=('DELETE', 'OPTIONS'))
def delete_one(request, name):
    return json(devices_resource().delete(request, name))


@app.route(ep_root + '/available', methods=('GET',))
def available_devices(request):
    return json(devices_resource().get_available_devices(request))


@app.route(ep_root + '/inuse', methods=('GET',))
def devices_inuse(request):
    return json(devices_resource().get_devices_inuse(request))
