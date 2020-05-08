"""Unit tests for the SchedulerStore."""
from io import BytesIO

import pytest

from apscheduler.schedulers.base import BaseScheduler

from poolctl.utils.misc import Undef
from poolctl.model.scheduler.custom_scheduler import CustomScheduler
from poolctl.model.scheduler.scheduler_store import SchedulerStore

from tests.unit_tests.model_tests.scheduler_tests.fake_stuff import (
    fake_random_record_as_dict,
)


class SampleScheduler(BaseScheduler):
    def shutdown(self, wait=True):
        pass

    def wakeup(self):
        pass


class TestSchedulerStore:

    def _fake_record(self):
        return fake_random_record_as_dict()

    def setup_method(self):
        scheduler = CustomScheduler()
        self.store = SchedulerStore(scheduler)

    def test_put_get__case_1(self):
        rec = self._fake_record()
        self.store.put(rec)
        loaded = self.store.get(rec['pkey'])
        assert loaded == rec

    def test_delete(self):
        rec = self._fake_record()
        self.store.put(rec)
        deleted = self.store.delete(rec['pkey'])
        assert deleted == rec
        assert deleted is not rec
        none = self.store.delete(rec['pkey'])
        assert none is None

    def test_get_all(self):
        rec_1 = self._fake_record()
        rec_2 = self._fake_record()
        self.store.put(rec_1)
        self.store.put(rec_2)
        assert self.store.get_all() == [rec_1, rec_2]
