"""
/records endpoint bindings.

Records denotes pool controller timetable/schedule records.
Each of these has ... TODO: describe briefly

"""
from functools import lru_cache

from sanic.log import logger as log
from sanic.exceptions import NotFound
from sanic.response import json, html

from poolctl.app import app, Runner
from poolctl.restapi.endpoints import API_ROOT

ep_root = API_ROOT + '/records'


@lru_cache(maxsize=1)
def records_resource():
    return Runner.instance().records_resource


@app.exception(NotFound)
async def status_404(request, exc):
    log.warning('file not found (404): relative_url=%r path=%r', exc.relative_url, exc.path)
    return json({
        'status': 'error',
        'message': f'not found: {exc.relative_url}',
    }, status=404)


def report_records_ep_availability():
    log.info(ep_root + ' endpoint imported and available')


@app.route('/')
async def test(request):
    log.info('request detected')
    return html('<h3>PoolCtl app works! ;)<h3>')


@app.route(ep_root, methods=['GET', 'POST', 'OPTIONS'])
def get_all_or_create(request):
    method = request.method.upper()
    func_map = {
        'GET': records_resource().get_all,
        'POST': records_resource().post,
    }
    return func_map[method](request)


@app.route(ep_root + '/<pkey:string>', methods=['GET'])
def get_one(request, pkey):
    return records_resource().get(request, pkey)


@app.route(ep_root + '/<pkey:string>', methods=['PUT'])
def put_one(request, pkey):
    return records_resource().put(request, pkey)


@app.route(ep_root + '/<pkey:string>', methods=['DELETE', 'OPTIONS'])
def delete_one(request, pkey):
    return records_resource().delete(request, pkey)
