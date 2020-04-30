"""Unit tests for the devices REST API resource."""

import pytest

from sanic.exceptions import NotFound, InvalidUsage, SanicException

from poolctl.model.devices.manager import DeviceManager
from poolctl.restapi.resources.devices import DevicesResource

from tests._utils.fixtures.fake_pi import __setup_teardown


@pytest.fixture(scope='function', autouse=True)
def devices_res(mocker):
    return DevicesResource(DeviceManager())


@pytest.fixture(scope='function', autouse=True)
def mock_request(mocker):
    return mocker.MagicMock()


def _post_some(devices_res, mock_request):
    mock_request.json = {
        'name': 'L2',
        'kind': 'light',
        'gpio': '9',
    }
    devices_res.post(mock_request)
    mock_request.json = {
        'name': 'P2',
        'kind': 'pump',
        'gpio': '7',
    }
    devices_res.post(mock_request)


def test_get_all__empty_backend(devices_res):
    assert devices_res.get_all() == {'status': 'success', 'devices': []}


def test_post_some__get_all(devices_res, mock_request):
    _post_some(devices_res, mock_request)
    expected = {
        'status': 'success',
        'devices': [
            {'active': False, 'duty_cycle': 0, 'gpio': 9, 'kind': 'light', 'name': 'L2'},
            {'active': False, 'duty_cycle': 0, 'gpio': 7, 'kind': 'pump', 'name': 'P2'},
        ],
    }
    assert devices_res.get_all() == expected


def test_put__try_recreating_device_with_same_name(devices_res, mock_request):
    mock_request.json = {
        'name': 'samename',
        'kind': 'relay',
        'gpio': '7',
    }
    devices_res.post(mock_request)
    mock_request.json = {
        'name': 'samename',
        'kind': 'pump',
        'gpio': '9',
    }
    try:
        devices_res.post(mock_request)
    except SanicException as err:
        assert err.status_code == 409
        assert err.args[0] == {'status': 'error', 'message': 'device with name=samename already exists'}


def test_put__try_recreating_device_with_same_pin(devices_res, mock_request):
    mock_request.json = {
        'name': 'D1',
        'kind': 'relay',
        'gpio': '7',
    }
    devices_res.post(mock_request)
    mock_request.json = {
        'name': 'P1',
        'kind': 'pump',
        'gpio': 7,
    }
    try:
        devices_res.post(mock_request)
    except SanicException as err:
        assert err.status_code == 409
        assert err.args[0] == {'status': 'error', 'message': 'pin 7 already in use'}


def test_put__try_recreating_device__wrong_kind(devices_res, mock_request):
    mock_request.json = {
        'name': 'D1',
        'kind': 'non-existent',
        'gpio': 7,
    }
    try:
        devices_res.post(mock_request)
    except InvalidUsage as err:
        assert err.status_code == 400
        assert err.args[0] == {'status': 'error', 'message': "illegal device kind 'non-existent'"}


# TODO: try creating device with incorrect pin

def test_delete(devices_res, mock_request):
    _post_some(devices_res, mock_request)
    mock_request.json = {}
    removed = devices_res.delete(mock_request, 'L2')
    expected_removed = {
        'status': 'success',
        'deleted_record': {'active': False, 'duty_cycle': 0, 'gpio': 9, 'kind': 'light', 'name': 'L2'},
    }
    assert removed == expected_removed
    expected = {
        'status': 'success',
        'devices': [{'active': False, 'duty_cycle': 0, 'gpio': 7, 'kind': 'pump', 'name': 'P2'}],
    }
    assert devices_res.get_all() == expected
    devices_res.delete(mock_request, 'P2')
    assert devices_res.get_all() == {'status': 'success', 'devices': []}


def test_delete__non_existent(devices_res):
    expected = {'status': 'error', 'message': "record not found for name 'non-existent'"}
    try:
        devices_res.delete(mock_request, 'non-existent')
    except NotFound as err:
        assert err.args[0] == expected


def test_get_available_devices__on_empty_backend(devices_res, mock_request):
    expected = {
        'status': 'success',
        'names': ['P1', 'P2', 'L1', 'L2', 'L3', 'L4', 'T', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'],
        'gpios': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
        'kinds': ['light', 'pump', 'relay'],
    }
    assert devices_res.get_available_devices(mock_request) == expected


def test_get_devices_inuse__on_empty_backend(devices_res, mock_request):
    assert devices_res.get_devices_inuse(mock_request) == {'status': 'success', 'names': []}


def test_get_devices_inuse(devices_res, mock_request):
    _post_some(devices_res, mock_request)
    assert devices_res.get_devices_inuse(mock_request) == {'status': 'success', 'names': ['P2', 'L2']}
