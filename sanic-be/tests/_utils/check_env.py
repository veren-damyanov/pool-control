"""
Check-environment helpers.

"""
from poolctl import settings as cfg


def check_environment():
    """Exit with lots of noise if environment is 'prod'.
    TODO: make sure check_environment() is invoked on each and every non-prod test exec!
    """
    if cfg.ENVIRONMENT_NAME.lower() == 'prod':
        message = 'CANNOT RUN TESTS ON **PROD** ENVIRONMENT'
        import sys
        print(message, file=sys.stderr)
        print(message, file=sys.stdout)
        import logging
        logging.getLogger().critical(message)
        raise SystemExit(message)
