"""
APScheduler-based schedule-record store.

"""
from __future__ import annotations

from typing import Optional, List

from poolctl.utils.misc import check_type, Undef, nameof
from poolctl.model.scheduler import both_or_none, raw_record
from poolctl.model.scheduler._types import SchedRecAsDictT, SchedulerStoreT
from poolctl.model.scheduler.custom_scheduler import CustomScheduler
from poolctl.model.scheduler.record_container import RecordContainer


class SchedulerStore(SchedulerStoreT):
    instance = None

    @classmethod
    def launch(cls, scheduler: CustomScheduler) -> SchedulerStore:
        assert not cls.instance, f'{nameof(cls)} singleton instance violation'
        cls.instance = SchedulerStore(scheduler)
        return cls.instance

    def __init__(self, scheduler: CustomScheduler):
        super().__init__()
        check_type(scheduler, CustomScheduler)
        self._scheduler = scheduler

    # @property
    # def device_manager(self):
    #     return self._device_manager

    def has(self, pkey: str) -> bool:
        return self.get(pkey) not in (None, Undef)

    def put(self, rec_dict: SchedRecAsDictT) -> None:
        record_obj = RecordContainer(rec_dict)
        self._scheduler.add_double_job(record_obj)

    @staticmethod
    def _one_for_identical_records(end_job, start_job, operation) -> Optional[SchedRecAsDictT]:
        message = f'inconsistent double job on {operation}: start_job={start_job}, end_job={end_job}'
        assert both_or_none(start_job, end_job), message
        if not start_job:
            return None
        start_raw_rec = raw_record(start_job)
        end_raw_rec = raw_record(end_job)
        message = f'inconsistent start/end raw records during get:' \
                  f' start_raw_rec={start_raw_rec}, end_raw_rec={end_raw_rec}'
        assert start_raw_rec == end_raw_rec, message
        return raw_record(start_job)

    def get(self, pkey: str) -> Optional[SchedRecAsDictT]:
        start_job, end_job = self._scheduler.get_double_job(pkey)
        return self._one_for_identical_records(end_job, start_job, 'get')

    def delete(self, pkey: str) -> Optional[SchedRecAsDictT]:
        start_job, end_job = self._scheduler.remove_double_job(pkey)
        return self._one_for_identical_records(end_job, start_job, 'delete')

    def get_all(self) -> List[SchedRecAsDictT]:
        return [raw_record(job) for job in self._scheduler.get_jobs() if job.id.endswith(':start')]

    def shutdown(self):
        pass
