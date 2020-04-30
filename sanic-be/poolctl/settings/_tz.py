"""
Infer server's timezone (supposedly same as the pool timezone).

"""
from typing import Optional
from datetime import datetime

import pytz

_TZ_FILE = '/etc/timezone'

TzOutcomeT = Optional[pytz.tzinfo.BaseTzInfo]


def determine_timezone(pool_timezone: str, tz_file=_TZ_FILE) -> TzOutcomeT:
    """Try to determine and retuen the timezone of the current back-end
    host as a pytz.tzinfo.BaseTzInfo object. Return ``None``

    :param pool_timezone str: timezone in
    :return BaseTzInfo: the timezone as a pytz.tzinfo.BaseTzInfo object
    """

    def determine_tz():
        # try with /etc/timezone
        try:
            with open(tz_file) as fd:
                return fd.read().strip()

        except FileNotFoundError:
            pass

        # try with /etc/localtime
        import os
        SEP = os.sep  # forward slash '/'
        try:
            path = os.readlink('/etc/localtime')
            if path.startswith('/usr/share/zoneinfo') and path.count(SEP) == 5:
                return SEP.join(path.split(SEP)[-2:])

        except Exception:
            pass

        # TODO: we can possibly use `timedatectl` or even have a REST API checking
        #       the location via GeoIP and returning the TZ (not to speak of a local
        #       GPS reporting the exact location)

        return None

    if pool_timezone:
        return pytz.timezone(pool_timezone)

    tz = determine_tz()
    if tz:
        return pytz.timezone(tz)

    return datetime.now().astimezone().tzinfo
