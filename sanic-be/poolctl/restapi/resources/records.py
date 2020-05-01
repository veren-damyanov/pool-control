"""
Web controller code for the "Pool Controller" application.
"""

from copy import copy

from sanic.response import json

from poolctl.utils.misc import check_type, random_string, Undef
from poolctl.model.scheduler._types import SchedulerStoreT
from ._common import abort_404, BaseResource


class RecordsResource(BaseResource):

    def __init__(self, store: SchedulerStoreT):
        check_type(store, SchedulerStoreT)
        self._store = store

    def get_all(self, order_by=None):  # TODO: implement sorting
        return json({
            'status': 'success',
            'records': [rec for rec in self._store.get_all()],
        })

    def get(self, request, pkey):
        rec = self._store.get(pkey)
        if rec is Undef:
            abort_404('record not found for pkey ' + pkey)

        return json({
            'status': 'success',
            'record': rec,
        })

    def post(self, request):
        rec = request.json
        # TODO: check request payload schema
        pkey = random_string()
        rec['pkey'] = pkey
        norm_rec = copy(rec)
        self._store.put(pkey, norm_rec)
        return json({
            'status': 'success',
            'record': norm_rec,
        })

    def put(self, request, pkey):
        rec = request.json
        # TODO: check request payload schema
        rec_pkey = str(rec['pkey'])
        assert rec_pkey == pkey, f'Key from url: {pkey}, and key from body: {rec_pkey} are not the same!'
        if not self._store.has(pkey):
            abort_404('record not found for pkey ' + pkey)

        norm_rec = copy(rec)
        self._store.put(pkey, norm_rec)
        return json({
            'status': 'success',
            'record': norm_rec,
        })

    def delete(self, request, pkey):
        rec = self._store.delete(pkey)
        if rec is Undef:
            abort_404('record not found for pkey ' + pkey)

        return json({
            'status': 'success',
            'deleted_record': rec,
        })
