"""
Unit tests for the DeviceManager.

"""
import pytest

from poolctl.model.devices.manager import DeviceManager

from tests._utils.fixtures.fake_pi import __setup_teardown


@pytest.fixture(autouse=True)
def manager():
    return DeviceManager()


def test_put_device__get_device(manager):
    manager.put_device('P1', 'pump', 3)
    device_rec = manager.get_device('P1')
    expected = {'active': False, 'duty_cycle': 0, 'gpio': 3, 'kind': 'pump', 'name': 'P1'}
    assert device_rec == expected


def test_delete_device(manager):
    manager.put_device('P2', 'pump', 7)
    manager.delete_device('P2')
    assert None is manager.get_device('P2')


def test_get_all__empty_manager_returns_empty_list(manager):
    assert [] == manager.get_all()


def test_get_all__returns_list(manager):
    manager.put_device('P1', 'pump', 7)
    manager.put_device('P2', 'pump', 3)
    expected = [
        {'active': False, 'duty_cycle': 0, 'gpio': 7, 'kind': 'pump', 'name': 'P1'},
        {'active': False, 'duty_cycle': 0, 'gpio': 3, 'kind': 'pump', 'name': 'P2'},
    ]
    assert manager.get_all() == expected


def test_get_all_names(manager):
    expected = ['P1', 'P2', 'L1', 'L2', 'L3', 'L4', 'T', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
    assert expected == manager.get_all_names()


def test_get_available_names__empty_manager_returns_all_as_available(manager):
    all_names = manager.get_all_names()
    assert manager.get_available_names() == all_names


def test_get_available_names__case_1(manager):
    manager.put_device('P1', 'pump', 7)
    expected = ['P2', 'L1', 'L2', 'L3', 'L4', 'T', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
    assert manager.get_available_names() == expected


def test_get_available_names__case_2(manager):
    device_data = [
        ('P1', 'pump', '7'),
        ('P2', 'pump', 5),
        ('D1', 'relay', 27),
        ('D2', 'relay', 23),
        ('D3', 'relay', 24),
        ('L3', 'light', 12),
    ]
    for name, kind, pin in device_data:
        manager.put_device(name, kind, pin)
    expected = ['L1', 'L2', 'L4', 'T', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
    assert manager.get_available_names() == expected


def test_get_available_gpios__empty_manager_returns_all_as_available(manager):
    expected = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    ]
    assert manager.get_available_gpios() == expected


def test_get_available_gpios__case_1(manager):
    manager.put_device('P1', 'pump', 7)
    expected = [
        1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    ]
    assert manager.get_available_gpios() == expected


def test_get_available_gpios__case_2(manager):
    device_data = [
        ('P1', 'pump', 7),
        ('P2', 'pump', 5),
        ('D1', 'relay', 27),
        ('D2', 'relay', 23),
        ('D3', 'relay', 24),
        ('L3', 'light', 12),
    ]
    for name, kind, pin in device_data:
        manager.put_device(name, kind, pin)
    expected = [
        1, 2, 3, 4, 6, 8, 9, 10, 11, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 25, 26,
    ]
    assert manager.get_available_gpios() == expected


def test_get_available_kinds(manager):
    expected = {'pump', 'light', 'relay'}
    assert set(manager.get_available_kinds()) == expected
    manager.put_device('P1', 'pump', 7)
    assert set(manager.get_available_kinds()) == expected


def test_get_devices_inuse__empty_manager_returns_empty_list(manager):
    assert manager.get_devices_inuse() == []


def test_get_devices_inuse__case_1(manager):
    manager.put_device('P1', 'pump', 7)
    expected = ['P1']
    assert manager.get_devices_inuse() == expected
