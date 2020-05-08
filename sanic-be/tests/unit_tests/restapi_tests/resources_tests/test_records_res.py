import pytest

from sanic.exceptions import NotFound, InvalidUsage

from poolctl.model.scheduler.custom_scheduler import CustomScheduler
from poolctl.model.scheduler.scheduler_store import SchedulerStore
from poolctl.restapi.resources.records import RecordsResource


@pytest.fixture(scope='function', autouse=True)
def records_res():
    return RecordsResource(SchedulerStore(CustomScheduler()))


def test_post_with_pkey_yields_400(records_res):
    post_payload = {
        'pkey': 'abcde',  # presence of this should cause 400
        'target': 'D9',
        'start_at': '1990-02-19T09:09+02:00',
        'end_at': '1990-02-19T19:19+02:00',
        'dow': ['TH', 'FR'],
        'value': 75,
    }
    try:
        records_res.post(post_payload)
    except InvalidUsage as err:
        assert err.status_code == 400
        assert err.args[0] == {'status': 'error', 'message': 'post payload cannot contain pkey'}
    else:
        pytest.fail('InvalidUsage NOT raised')


def test_post_with_empty_pkey_works_fine(records_res):
    post_payload = {
        'pkey': None,
        'target': 'D25',
        'start_at': '1990-02-19T09:09+02:00',
        'end_at': '1990-02-19T19:19+02:00',
        'dow': ['TH', 'FR'],
        'value': 25,
    }
    records_res.post(post_payload)
    post_payload = {
        'pkey': '',
        'target': 'D50',
        'start_at': '1990-02-19T09:09+02:00',
        'end_at': '1990-02-19T19:19+02:00',
        'dow': ['TH', 'FR'],
        'value': 50,
    }
    records_res.post(post_payload)


def test_get_nonexistent_yields_404(records_res):
    try:
        records_res.get('non-existent')
    except NotFound as err:
        assert err.status_code == 404
        assert err.args[0] == {'status': 'error', 'message': 'record not found for pkey non-existent'}
    else:
        pytest.fail('NotFound NOT raised')


def test_put_nonexistent_yields_404(records_res):
    pkey = 'non-existent'
    post_payload = {
        'pkey': pkey,
        'target': 'L0',
        'start_at': '1990-02-19T00:00+02:00',
        'end_at': '1990-02-19T00:00+02:00',
        'dow': ['MO'],
        'value': 0,
    }
    try:
        records_res.put(post_payload, pkey)
    except NotFound as err:
        assert err.status_code == 404
        assert err.args[0] == {'status': 'error', 'message': 'record not found for pkey non-existent'}
    else:
        pytest.fail('NotFound NOT raised')


def test_delete_nonexistent_yields_404(records_res):
    try:
        records_res.delete('non-existent')
    except NotFound as err:
        assert err.status_code == 404
        assert err.args[0] == {'status': 'error', 'message': 'record not found for pkey non-existent'}
    else:
        pytest.fail('NotFound NOT raised')


def test_post_then_get_record(records_res):
    post_payload = {
        'target': 'L4',
        'start_at': '1990-02-19T08:09+02:00',
        'end_at': '1990-02-19T20:14+02:00',
        'dow': ['TH', 'FR', 'SA'],
        'value': 50,
    }
    post_result = records_res.post(post_payload)
    record = post_result['record']
    partial = record.copy()
    del partial['pkey']
    assert partial == post_payload
    get_result = records_res.get(record['pkey'])
    loaded_record = get_result['record']
    del loaded_record['pkey']
    assert loaded_record == post_payload


def test_post_then_put_then_get(records_res):
    post_payload = {
        'target': 'L2',
        'start_at': '1990-02-19T02:22+02:00',
        'end_at': '1990-02-19T22:02+02:00',
        'dow': ['FR', 'SA', 'SU'],
        'value': 25,
    }
    post_result = records_res.post(post_payload)
    pkey = post_result['record']['pkey']
    put_payload = {
        'pkey': pkey,
        'target': 'L2',
        'start_at': '1990-02-19T03:33+02:00',
        'end_at': '1990-02-19T23:33+02:00',
        'dow': ['FR'],
        'value': 50,
    }
    put_result = records_res.put(put_payload, pkey)
    expected = {'status': 'success',
                'record': {'pkey': pkey, 'target': 'L2', 'start_at': '1990-02-19T03:33+02:00',
                           'end_at': '1990-02-19T23:33+02:00', 'dow': ['FR'], 'value': 50}}
    assert put_result == expected


def test_post_then_double_delete(records_res):
    post_payload = {
        'target': 'D2',
        'start_at': '1990-02-19T22:02+02:00',
        'end_at': '1990-02-19T02:22+02:00',
        'dow': ['SU'],
        'value': 25,
    }
    post_result = records_res.post(post_payload)
    pkey = post_result['record']['pkey']
    delete_result = records_res.delete(pkey)
    expected = {'status': 'success',
                'deleted_record': {'target': 'D2', 'start_at': '1990-02-19T22:02+02:00',
                                   'end_at': '1990-02-19T02:22+02:00', 'dow': ['SU'], 'value': 25,
                                   'pkey': pkey}}
    assert delete_result == expected
    try:
        records_res.delete(pkey)
    except NotFound as err:
        assert err.status_code == 404
        assert err.args[0] == {'status': 'error', 'message': 'record not found for pkey ' + pkey}
    else:
        pytest.fail('NotFound NOT raised')
