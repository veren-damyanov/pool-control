"""
TODO:

"""
from sanic.log import logger as log
from apscheduler.schedulers.base import BaseScheduler

from poolctl.utils.misc import check_type, typeof, Undef
from poolctl.model.scheduler._types import SchedRecordT, SchedulerStoreT
from poolctl.model.scheduler.tasks import switch_device_on, switch_device_off
from poolctl.model.scheduler.record_container import RecordContainer
from poolctl.model.devices.manager import DeviceManager


def raw_record(job):
    return job.args[1].raw_data


class SchedulerStore(SchedulerStoreT):

    def __init__(self, scheduler: BaseScheduler, device_manager: DeviceManager):
        check_type(scheduler, BaseScheduler)
        check_type(device_manager, DeviceManager)
        self._scheduler = scheduler
        self._device_manager = device_manager

    def has(self, pkey: str) -> bool:
        return self.get(pkey) not in (None, Undef)

    def _get_double_jobs(self, record_obj):
        return (
            self._scheduler.get_job(job_id=record_obj.id + ':start'),
            self._scheduler.get_job(job_id=record_obj.id + ':end'),
        )

    def _both_or_none(self, start_job, end_job):
        return bool(start_job) == bool(end_job)

    def _schedule_job(self, record_obj):
        start_hour, start_minute = record_obj.start_at_hour_minute()
        end_hour, end_minute = record_obj.end_at_hour_minute()
        try:
            self._scheduler.add_job(
                switch_device_on,
                'cron',
                (self._device_manager, record_obj,),
                day_of_week=record_obj.dow,
                hour=start_hour,
                minute=start_minute,
                id=record_obj.id + ':start',
                name=record_obj.name,
                replace_existing=True,
            )
            self._scheduler.add_job(
                switch_device_off,
                'cron',
                (self._device_manager, record_obj,),
                day_of_week=record_obj.dow,
                hour=end_hour,
                minute=end_minute,
                id=record_obj.id + ':end',
                name=record_obj.name,
                replace_existing=True,
            )
            log.info(f'scheduled jobs for start={start_hour}:{start_minute}, end={end_hour}:{end_minute}')

        except Exception as orig_err:
            try:
                self._scheduler.remove_job(job_id=record_obj.id + ':start')
            except Exception as err:
                log.error(f"Error trying to remove job {record_obj.id + ':start'}: {typeof(err)}: {err}")

            try:
                self._scheduler.remove_job(job_id=record_obj.id + ':end')
            except Exception as err:
                log.error(f"Error trying to remove job {record_obj.id + ':end'}: {typeof(err)}: {err}")

            raise orig_err

        finally:
            start_job, end_job = self._get_double_jobs(record_obj)
            message = f'inconsistent double job state after put: start_job={start_job}, end_job={end_job}'
            assert self._both_or_none(start_job, end_job), message

    def put(self, pkey: str, payload: SchedRecordT):
        record_obj = RecordContainer(payload)
        self._schedule_job(record_obj)

    def get(self, pkey: str) -> SchedRecordT:
        start_job = self._scheduler.get_job(pkey + ':start')
        end_job = self._scheduler.get_job(pkey + ':end')
        message = f'inconsistent double job during get: start_job={start_job}, end_job={end_job}'
        assert self._both_or_none(start_job, end_job), message
        if not start_job:
            return Undef
        start_raw_rec = raw_record(start_job)
        end_raw_rec = raw_record(end_job)
        message = f'inconsistent start/end raw records during get:' \
                  f' start_raw_rec={start_raw_rec}, end_raw_rec={end_raw_rec}'
        assert start_raw_rec == end_raw_rec, message
        return raw_record(start_job)

    def delete(self, pkey: str) -> SchedRecordT:
        start_job = self._scheduler.get_job(pkey + ':start')
        end_job = self._scheduler.get_job(pkey + ':end')
        message = f'inconsistent double job before delete: start_job={start_job}, end_job={end_job}'
        assert self._both_or_none(start_job, end_job), message
        if not start_job:
            return Undef
        # Now JobLookupError is not expected to pop up
        try:
            self._scheduler.remove_job(pkey + ':start')
        except Exception as err:
            print(f"Error trying to delete start_job={start_job}: {typeof(err)}: {err}")

        try:
            self._scheduler.remove_job(pkey + ':end')
        except Exception as err:
            print(f"Error trying to delete end_job={end_job}: {typeof(err)}: {err}")

        start_job_none = self._scheduler.get_job(pkey + ':start')
        end_job_none = self._scheduler.get_job(pkey + ':end')
        message = f'inconsistent double job after delete: start_job={start_job}, end_job={end_job}'
        assert not (start_job_none or end_job_none), message

        start_raw_rec = raw_record(start_job)
        end_raw_rec = raw_record(end_job)
        message = f'inconsistent start/end raw records during get:' \
                  f' start_raw_rec={start_raw_rec}, end_raw_rec={end_raw_rec}'
        assert start_raw_rec == end_raw_rec, message
        return raw_record(start_job)

    def get_all(self):
        return [raw_record(job) for job in self._scheduler.get_jobs() if job.id.endswith(':start')]

    @classmethod
    def launch(cls, scheduler: BaseScheduler, device_manager: DeviceManager):
        store = cls(scheduler, device_manager)
        scheduler.start()
        return store

    def shutdown(self):
        self._scheduler.shutdown()
        self._device_manager.shutdown()
