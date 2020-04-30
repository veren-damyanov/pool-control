"""
utils.misc module unit tests.
"""

import pytest

from poolctl.utils.misc import typeof, nameof, check_type


def test_typeof():
    assert 'str' == typeof('string')
    assert 'int' == typeof(42)
    assert 'NoneType' == typeof(None)


def test_nameof():
    assert 'str' == nameof(str)
    assert 'int' == nameof(int)


def test_nameof__non_type_raises_error():
    with pytest.raises(AssertionError):
        nameof('not-a-type')


def test_check_type__ok():
    check_type('string', str)
    check_type(42, int)
    check_type(42, (float, complex, int))


def test_check_type__raise_typeerror():
    with pytest.raises(TypeError):
        check_type('string', (list, tuple, dict))
    with pytest.raises(TypeError):
        check_type(42, (complex, float))
