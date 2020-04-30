"""
Pool Control settings override logic.

ENVIRONMENT_NAME can be one of:
- local - local development/testing env.
- integration - CI integration env.
- stage - Stage env.
- prod - Prod env. - regular tests should refuse to run in Prod

Environments may have flavors (these are mostly modes on the same env) like:

- local:dev
- local:mocktest
- local:livetest

- stage:mocktest
- stage:livetest
- stage:preprod

'prod' does not have flavours - it means we are running live on customer hardware!

"""
import os
import sys

from ._tz import determine_timezone
from ._default import *

_ACCEPTABLE_ENVIRONMENTS = (
    'local',
    'integration',
    'stage',
    'prod',
)

ENVIRONMENT_NAME = os.environ.get('ENVIRONMENT_NAME', 'local')
ENVIRONMENT_BASE, ENVIRONMENT_FLAVOR = (ENVIRONMENT_NAME + ':none').split(':', 1)[:2]
assert ENVIRONMENT_BASE in _ACCEPTABLE_ENVIRONMENTS, f'Unacceptable environment {ENVIRONMENT_BASE!r}'

POOL_TIMEZONE = None  # some of the files imported below may override this.

exec(f'from .{ENVIRONMENT_BASE} import *')

try:  from ._local import *
except ModuleNotFoundError:  pass

POOL_TZ = determine_timezone(POOL_TIMEZONE)
assert POOL_TZ, 'FATAL: Could NOT determine server timezone'

print('+++ ENVIRONMENT:', ENVIRONMENT_BASE, ENVIRONMENT_FLAVOR, file=sys.stderr)
