"""Miscellaneous utilities."""

import random
import string


class UndefType(object):
    """A kind with a single instance denoting an undefined value."""
    def __str__(self): return ':Undef:'
    def __bool__(self): return False
    __repr__ = __str__


Undef = UndefType()

NoneType = type(None)


def typeof(obj: object) -> str:
    """Return this objects class name."""
    return obj.__class__.__name__


def nameof(klass) -> str:
    """Return this klass' name."""
    assert isinstance(klass, type)
    return klass.__name__


def check_type(obj, types):
    """Raise TypeError if given obj is not of given kind(s), otherwise pass silently."""
    if not isinstance(obj, types):
        raise TypeError(f'expected {types}, got {obj!r} of {type(obj)}')


def random_string(size=4, chars=string.ascii_lowercase):
    """Return a random string with length ``size`` containing characters
    picked from ``chars``.
    """
    return ''.join(random.choice(chars) for _ in range(size))
