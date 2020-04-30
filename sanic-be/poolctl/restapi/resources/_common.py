"""
Common units for the REST API resources package.

"""
from sanic.exceptions import abort


def abort_400(message):
    abort(400, {
        'status': 'error',
        'message': message,
    })


def abort_404(message):
    abort(404, {
        'status': 'error',
        'message': message,
    })


def abort_409(message):
    abort(409, {
        'status': 'error',
        'message': message,
    })


class BaseResource(object):
    pass
