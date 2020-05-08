"""
Stage environment settings.

See __init__ docstring for environment setup details.

"""

# Listen on the local interface to mimic closely the prod environment
APP_ARGS = {
    'host': '127.0.0.1',
    'port': 8000,
    'debug': False,
}
