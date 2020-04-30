"""
Sample for optional custom _local settings.

Copy this file into `_local.py` and tune it to suit
your needs. Variables set here would override their
setup values from any other environment setup file.

See __init__ docstring for environment setup details.

"""

#: Host and port for connecting to the pigpiod daemon.
#: For production, the host is typically 'localhost', but
#: remote connections are possible - make sure the remote
#: pi firewall (if any) allows the connection and pigpiod
#: listens on external interface(s).
PIGPIOD_HOST = '10.11.12.13'
PIGPIOD_PORT = 8888

#: A PIGPIOD_HOST value starting with "FAKE" would end up configuring
#: a mock connection for environments where a real pi is not available
#: or not convenient to use.
PIGPIOD_HOST = 'FAKE-PIGPIOD-HOST'

#: You might want to fix issues with broken time zone OS setup
#: defining the "real one"(tm) here.
POOL_TIMEZONE = 'Europe/Sofia'

#: You may also wish to tune the app start arguments (most probably
#: the port and/or the debug mode).
APP_ARGS = {
    'host': '0.0.0.0',
    'port': 9090,
    'debug': False,
}
