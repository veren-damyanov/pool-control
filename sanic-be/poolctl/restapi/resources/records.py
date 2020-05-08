"""
Web controller code for the "Pool Controller" application.
"""

from copy import copy

from sanic.log import logger as log

from poolctl.utils.misc import check_type, random_string, Undef
from poolctl.model.scheduler._types import SchedulerStoreT
from ._common import BaseResource, abort_400, abort_404


class RecordsResource(BaseResource):

    def __init__(self, store: SchedulerStoreT):
        check_type(store, SchedulerStoreT)
        self._store = store

    def get_all(self, payload=None, order_by=None):  # TODO: implement sorting
        log.debug('get_all /records')
        return {
            'status': 'success',
            'records': [rec for rec in self._store.get_all()],
        }

    def get(self, pkey):
        log.debug('get /records/%s', pkey)
        rec = self._store.get(pkey)
        if not rec:
            abort_404('record not found for pkey ' + pkey)

        return {
            'status': 'success',
            'record': rec,
        }

    def post(self, payload):
        log.debug('post /records %r', payload)
        rec = copy(payload)
        # TODO: check payload payload schema
        if rec.get('pkey'):
            abort_400('post payload cannot contain pkey')
        pkey = random_string()
        rec['pkey'] = pkey
        norm_rec = copy(rec)
        self._store.put(norm_rec)
        return {
            'status': 'success',
            'record': norm_rec,
        }

    def put(self, payload, pkey):
        log.debug('put /records/%s %r', pkey, payload)
        rec = copy(payload)
        # TODO: check payload payload schema
        rec_pkey = str(rec['pkey'])
        assert rec_pkey == pkey, f'Key from url: {pkey}, and key from body: {rec_pkey} are not the same!'
        if not self._store.has(pkey):
            abort_404('record not found for pkey ' + pkey)

        norm_rec = copy(rec)
        self._store.put(norm_rec)
        return {
            'status': 'success',
            'record': norm_rec,
        }

    def delete(self, pkey):
        log.debug('delete /records/%s', pkey)
        rec = self._store.delete(pkey)
        if not rec:
            abort_404('record not found for pkey ' + pkey)

        return {
            'status': 'success',
            'deleted_record': rec,
        }
