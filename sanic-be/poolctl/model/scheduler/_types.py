"""
Scheduler model types.

"""
from typing import Union, Optional, List, Dict
from poolctl.utils.misc import UndefType

SchedRecAsDictT = Dict[str, Union[str, int]]


class SchedulerStoreT(object):
    """SchedulerStore interface"""

    def has(self, pkey: str) -> bool:
        raise NotImplementedError

    def put(self, rec_dict: SchedRecAsDictT) -> None:
        raise NotImplementedError

    def get(self, pkey: str) -> Optional[SchedRecAsDictT]:
        raise NotImplementedError

    def delete(self, pkey: str) -> Optional[SchedRecAsDictT]:
        raise NotImplementedError

    def get_all(self) -> List[SchedRecAsDictT]:
        raise NotImplementedError
