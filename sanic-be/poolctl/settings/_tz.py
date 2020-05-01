"""
Infer server's timezone on Linux (supposedly same as the pool timezone).

"""
from typing import Optional
from datetime import datetime

import pytz

_TZ_FILE = '/etc/timezone'
_LT_FILE = '/etc/localtime'
_ZONEINFO_HOME = '/usr/share/zoneinfo'

TzOutcomeT = Optional[pytz.tzinfo.BaseTzInfo]


def determine_timezone(pool_timezone: Optional[str], tz_file=_TZ_FILE) -> TzOutcomeT:
    """Try to determine and retuen the timezone of the current back-end
    host as a pytz.tzinfo.BaseTzInfo object. Return ``None``

    :param pool_timezone str: timezone in
    :return BaseTzInfo: the timezone as a pytz.tzinfo.BaseTzInfo object
    """

    def determine_tz():
        """If on Linux, try to find and return time zone information checking
        /etc/timezone, then /etc/localtime. Return None if none of these succeeds.
        """
        import platform
        if platform.system().lower() != 'linux':
            return None  # determine_tz() is for Linux only

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
            path = os.readlink(_LT_FILE)
            if path.startswith(_ZONEINFO_HOME) and path.count(SEP) == 5:
                # we have full path containing continent AND city
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
