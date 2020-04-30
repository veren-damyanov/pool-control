"""
TODO:

"""
from copy import deepcopy
from datetime import datetime

from poolctl import settings as cfg


class RecordContainer(object):
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f'Object of <type RecordContainer> has no attribute {name!r}')

    def __repr__(self):
        return f'<RecordContainer(id={self.id!r}, target={self.target!r}, timing: {self.timing})>'

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f'{self.target}={self.value} ({self.timing} dow={self.dow} id={self.id!r})'

    def start_at_hour_minute(self, tz=None):
        tz = tz or cfg.POOL_TZ
        start_at_intz = datetime.fromisoformat(self._data['start_at']).astimezone(tz)
        return start_at_intz.hour, start_at_intz.minute

    def end_at_hour_minute(self, tz=None):
        tz = tz or cfg.POOL_TZ
        end_at_intz = datetime.fromisoformat(self._data['end_at']).astimezone(tz)
        return end_at_intz.hour, end_at_intz.minute

    @property
    def timing(self):
        start_h, start_m = self.start_at_hour_minute()
        end_h, end_m = self.end_at_hour_minute()
        return f'{start_h:02d}:{start_m:02d} - {end_h:02d}:{end_m:02d}'

    @property
    def raw_data(self):
        return deepcopy(self._data)

    DOW_MAP = {
        'mo': 0,
        'tu': 1,
        'we': 2,
        'th': 3,
        'fr': 4,
        'sa': 5,
        'su': 6,
        'MO': 0,
        'TU': 1,
        'WE': 2,
        'TH': 3,
        'FR': 4,
        'SA': 5,
        'SU': 6,
    }

    @classmethod
    def _dow_as_day_of_week_arg_OLD(cls, record):
        return ','.join(
            str(cls.DOW_MAP[day])
            for day in cls.DOW_MAP.keys()
            if record[day]
        )

    @classmethod
    def _dow_as_day_of_week_arg(cls, record):
        return ','.join(
            map(str, sorted(cls.DOW_MAP[day] for day in record['dow']))
        )

    @property
    def dow(self):
        return self._dow_as_day_of_week_arg(self._data)

    @property
    def id(self):
        return self._data['pkey']
