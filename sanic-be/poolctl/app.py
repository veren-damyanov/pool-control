"""
Sanic application execution module.

"""
from sanic import Sanic
from sanic_cors import CORS
from sanic.log import logger as log
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import NotFound, ServerError, InvalidUsage

from poolctl import settings as cfg
from poolctl.utils.misc import typeof
from poolctl.utils.async_stuff import all_tasks_to_close
from poolctl.runner import Runner


def create_app() -> Sanic:
    app = Sanic('poolctl-be', load_env=False)
    CORS(app)  # TODO: Revisit security
    return app


app = create_app()


@app.exception(InvalidUsage)
def handle_400(request, exc):
    def r_dump(r: Request) -> str:
        return f'<Request {r.method} {r.url} headers={r.headers!r} body={r.body}>'

    log.error('Bad Request (400): %s for request=%s', exc, r_dump(request))
    return json({
        'status': 'error',
        'message': str(exc),
    }, status=400)


@app.exception(NotFound)
def handle_404(request, exc):
    log.warning('Not Found (404): %s', exc)
    return json({
        'status': 'error',
        'message': str(exc),
    }, status=404)


@app.exception(NotFound)
def handle_409(request, exc):
    log.warning('Conflict (409): %s', exc)
    return json({
        'status': 'error',
        'message': str(exc),
    }, status=409)


@app.exception(ServerError, Exception)
def handle_500(request, exc):
    log.error('internal server error (500): %s: %s', typeof(exc), exc, exc_info=True)
    return json({
        'status': 'error',
        'message': 'internal server error - see server logs',
    }, status=500)


@app.listener('before_server_start')
async def initialize_scheduler(app, loop):
    from poolctl.settings import _logging
    _logging.announce_logging_availability()
    log.info('Server starting up...')
    log.info('%r', {nm: getattr(cfg, nm) for nm in dir(cfg) if nm.isupper() and not nm.startswith('_')})
    app.runner = Runner.instance(loop)
    await app.runner.launch()


@app.listener('after_server_stop')
async def async_notify_server_stopping(app, loop):
    log.info('Back-end shutting down...')
    await app.runner.shutdown()
    await all_tasks_to_close()
    log.info('Back-end shut down cleanly.')
