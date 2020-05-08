"""
Unit tests for the DeviceManager.

"""
import pickle
from io import BytesIO

import pytest

from poolctl.model.devices.named import PumpDriver
from poolctl.model.devices.manager import DeviceManager

from tests._utils.fixtures.fake_pi import __setup_teardown  # do NOT remove


@pytest.fixture(autouse=True)
def manager():
    DeviceManager.instance = None  # allow calls to from_persistent_data()
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
    expected = ['P1', 'P2', 'L1', 'L2', 'L3', 'L4', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
    assert expected == manager.get_all_names()


def test_get_available_names__empty_manager_returns_all_as_available(manager):
    all_names = manager.get_all_names()
    assert manager.get_available_names() == all_names


def test_get_available_names__case_1(manager):
    manager.put_device('P1', 'pump', 7)
    expected = ['P2', 'L1', 'L2', 'L3', 'L4', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
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
    expected = ['L1', 'L2', 'L4', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9']
    assert manager.get_available_names() == expected


def test_get_available_gpios__empty_manager_returns_all_as_available(manager):
    expected = [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
    ]
    assert manager.get_available_gpios() == expected


def test_get_available_gpios__case_1(manager):
    manager.put_device('P1', 'pump', 7)
    expected = [
        2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15,
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
        2, 3, 4, 6, 8, 9, 10, 11, 13, 14, 15,
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


def test_is_dirty__set_clean(manager):
    assert manager.is_dirty() is False
    manager.put_device('P77', 'pump', 7)
    assert manager.is_dirty() is True
    manager.set_clean()
    assert manager.is_dirty() is False
    manager.delete_device('P77')
    assert manager.is_dirty() is True
    manager.set_clean()
    assert manager.is_dirty() is False


def test_persistent_data(manager):
    assert manager.persistent_data() is None
    manager.put_device('P88', 'pump', 8)
    data = manager.persistent_data()
    assert isinstance(data, dict)
    assert list(data.keys()) == ['P88']
    expected = {'kind': 'pump', 'name': 'P88', 'pin': 8}
    assert list(data.values())[0] == expected


@pytest.mark.asyncio
async def test_manager_is_clean_after_construction_from_persistent_data(manager):
    fd = BytesIO()
    manager.put_device('P55', 'pump', 5)
    await manager.persist(fd)
    manager.shutdown()  # free all pins, etc.
    manager.instance = None  # cleanup before creating a new instance
    DeviceManager.persistent_file = fd
    loaded_manager = await DeviceManager.from_persistent_data()
    assert loaded_manager.is_dirty() is False


@pytest.mark.asyncio
async def test_persist(manager):
    manager.put_device('P99', 'pump', 9)
    fd = BytesIO()
    await manager.persist(fd)
    initial_data = manager._persistent_data()
    pickled_data = fd.getvalue()
    manager.shutdown()  # need to free gpio pins
    loaded_manager = await DeviceManager.from_persistent_data(BytesIO(pickled_data))
    assert loaded_manager._persistent_data() == initial_data
    print(initial_data)


def test_manager_is_dirty_after_put(manager):
    assert manager.is_dirty() is False
    manager.put_device('P33', 'pump', 3)
    assert manager.is_dirty() is True


def test_manager_is_dirty_after_delete(manager):
    manager.put_device('P331', 'pump', 3)
    manager.set_clean()
    assert manager.is_dirty() is False
    manager.delete_device('P331')
    assert manager.is_dirty() is True
