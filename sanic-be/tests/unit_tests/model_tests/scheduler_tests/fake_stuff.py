import random
from datetime import datetime
from dataclasses import dataclass

from poolctl import settings as cfg
from poolctl.utils.misc import random_string

TARGETS = ('P1', 'P2', 'L1', 'L2', 'T', 'D1', 'D2', 'D3', 'D4')
INTENSITY = (0, 25, 50, 75, 100)
TEMPERATURE = (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34)
SWITCH = ('ON', 'OFF')
WEEK_DAYS = ('MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU')


def fake_value_for(target):
    first_ch = target[0]
    if first_ch in ('P', 'L'):
        return random.choice(INTENSITY)
    if first_ch == 'T':
        return random.choice(TEMPERATURE)
    if first_ch == 'D':
        return random.choice(SWITCH)
    raise RuntimeError('UNREACHABLE')


@dataclass
class HourMin:
    hour: int
    minute: int

    def __post_init__(self):
        assert 0 <= self.hour < 24, f'Illegal time: {self.hour}:{self.minute}'
        assert 0 <= self.minute < 60, f'Illegal time: {self.hour}:{self.minute}'

    def __str__(self):
        return f'{self.hour}:{self.minute}'

    @classmethod
    def from_str(cls, timestr):
        hour, minute = map(int, timestr.split(':'))
        return HourMin(hour, minute)


def random_time():
    return HourMin(random.randint(0, 23), random.randint(0, 59))
    # return datetime(2020, 3, random.randint(25, 30), random.randint(0, 23), random.randint(0, 59), 0)


def random_time_as_dict(tz=None):
    tz = tz or cfg.POOL_TZ
    dt = tz.localize(datetime(1990, 2, 19, random.randint(0, 23), random.randint(0, 59)))
    return dt.isoformat()


def fake_random_record_as_dict() -> dict:
    target = random.choice(TARGETS)
    record = {
        'pkey': random_string(),
        'target': target,
        'value': fake_value_for(target),
        'start_at': random_time_as_dict(),
        'end_at': random_time_as_dict(),
        'dow': [day for day in WEEK_DAYS if random.choice((True, False))]
    }
    return record
