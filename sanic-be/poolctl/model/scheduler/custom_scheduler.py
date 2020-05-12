"""
Custom scheduler abel to persist state in a pickled file, assuming
the exact type of jobs we put in it.

"""
from typing import Optional
from collections import OrderedDict

from sanic.log import logger as log
from apscheduler.schedulers.asyncio import AsyncIOScheduler, run_in_event_loop

from poolctl.utils.misc import typeof
from poolctl.model import PERSIST_DEVICES_JOB_ID, PERSIST_SCHEDULE_JOB_ID
from poolctl.model.scheduler import both_or_none, raw_record
from poolctl.model.mixins import PersistMixin
from .record_container import RecordContainer
from .tasks import switch_device_off, switch_device_on


class CustomScheduler(AsyncIOScheduler, PersistMixin):  # PersistMixin must be last to not overshadow Scheduler methods

    @classmethod
    async def _from_persistent_data(cls, data: Optional[dict], **kw) -> PersistMixin:
        scheduler = CustomScheduler(event_loop=kw.pop('event_loop', None))
        if data:
            for dict_record in data.values():
                scheduler._add_double_job(RecordContainer(dict_record))
        scheduler.set_clean()
        return scheduler

    def __init__(self, **kw):
        super().__init__(**kw)

    def _persistent_data(self) -> dict:
        jobs = self.get_jobs()
        result = OrderedDict()  # explicitly preserve order
        for job in jobs:
            if job.id in (PERSIST_DEVICES_JOB_ID, PERSIST_SCHEDULE_JOB_ID):  # skip the 'persist_state' job
                continue
            rec = raw_record(job)
            result[rec['pkey']] = rec.copy()
        return result

    def get_double_job(self, pkey: str):
        return (
            self.get_job(job_id=(pkey + ':start')),
            self.get_job(job_id=(pkey + ':end')),
        )

    def remove_double_job(self, pkey: str):
        start_job, end_job = self.get_double_job(pkey)
        message = f'inconsistent double job before remove_double_job: start_job={start_job}, end_job={end_job}'
        assert both_or_none(start_job, end_job), message
        if not start_job:
            return None, None

        # Now JobLookupError is not expected to pop up
        try:
            self.remove_job(pkey + ':start')
            self.remove_job(pkey + ':end')
        except Exception as err:
            log.error('Error trying to delete end_job=%r: %s: %s', start_job, typeof(err), err)

        start_job_none, end_job_none = self.get_double_job(pkey)
        message = f'inconsistent double job after delete: start_job={start_job}, end_job={end_job}'
        assert not (start_job_none or end_job_none), message
        self.set_dirty()
        return start_job, end_job

    def add_double_job(self, record_obj: RecordContainer):
        """Wraps _add_double_job with added call to set_dirty()."""
        start_job, end_job = self._add_double_job(record_obj)
        if start_job:  # and end_job, implicitly
            self.set_dirty()

    def _add_double_job(self, record_obj: RecordContainer):
        start_hour, start_minute = record_obj.start_at_hour_minute()
        end_hour, end_minute = record_obj.end_at_hour_minute()

        # DEBUG purposes: setup a job 5 seconds from now regardless of
        # the timing set in the schedule record, to speed up debugging.
        #
        # now = datetime.now()
        # in_a_moment = now + timedelta(seconds=5)
        # start_hour = in_a_moment.hour
        # start_minute = in_a_moment.minute
        # start_second = in_a_moment.second
        #
        # in_a_moment = now + timedelta(seconds=10)
        # end_hour = in_a_moment.hour
        # end_minute = in_a_moment.minute
        # end_second = in_a_moment.second

        try:
            self.add_job(
                switch_device_on,
                'cron',
                (record_obj,),
                day_of_week=record_obj.dow,
                hour=start_hour,
                minute=start_minute,
                second=1,
                # second=start_second,
                id=record_obj.id + ':start',
                name=record_obj.name,
                replace_existing=True,
            )
            self.add_job(
                switch_device_off,
                'cron',
                (record_obj,),
                day_of_week=record_obj.dow,
                hour=end_hour,
                minute=end_minute,
                second=0,
                # second=end_second,
                id=record_obj.id + ':end',
                name=record_obj.name,
                replace_existing=True,
            )
            log.info(f'scheduled jobs for start={start_hour}:{start_minute}, end={end_hour}:{end_minute}')

        except Exception as orig_err:
            full_pkey = record_obj.id + ':start'
            try:
                self.remove_job(job_id=full_pkey)
            except Exception as err:
                log.error(f"Error trying to remove job {full_pkey}: {typeof(err)}: {err}")

            full_pkey = record_obj.id + ':end'
            try:
                self.remove_job(job_id=full_pkey)
            except Exception as err:
                log.error(f"Error trying to remove job {full_pkey}: {typeof(err)}: {err}")

            raise orig_err

        finally:
            start_job, end_job = self.get_double_job(record_obj.id)
            message = f'inconsistent double job state after put: start_job={start_job}, end_job={end_job}'
            assert both_or_none(start_job, end_job), message
            return start_job, end_job
