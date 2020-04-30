"""
Scheduler model types.

"""
from typing import Union, Optional, List
from poolctl.utils.misc import UndefType

SchedRecordT = Union[dict, UndefType]


class SchedulerStoreT(object):
    """SchedulerStore interface"""

    def has(self, pkey: str) -> bool:
        raise NotImplementedError

    def put(self, pkey: str, payload: SchedRecordT):
        raise NotImplementedError

    def get(self, pkey: str) -> Optional[SchedRecordT]:
        raise NotImplementedError

    def delete(self, pkey: str) -> Optional[SchedRecordT]:
        raise NotImplementedError

    def get_all(self) -> List[SchedRecordT]:
        raise NotImplementedError
