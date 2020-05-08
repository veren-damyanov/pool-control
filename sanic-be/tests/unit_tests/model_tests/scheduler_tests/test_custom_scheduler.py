from io import BytesIO

import pytest

from poolctl.model.scheduler.record_container import RecordContainer
from poolctl.model.scheduler.custom_scheduler import CustomScheduler


@pytest.fixture(autouse=True)
def scheduler() -> CustomScheduler:
    CustomScheduler.instance = None  # allow calls to from_persistent_data()
    return CustomScheduler()


def test__persistent_data(scheduler: CustomScheduler):
    rec_obj = RecordContainer({
        'pkey': 'lumar',
        'target': 'L1',
        'start_at': '1990-02-19T08:06+02:00',
        'end_at': '1990-02-19T20:11+02:00',
        'dow': ['WE', 'TH', 'FR'],
        'value': 0
    })
    scheduler.add_double_job(rec_obj)
    expected = {'lumar': {'pkey': 'lumar', 'target': 'L1', 'start_at': '1990-02-19T08:06+02:00',
                          'end_at': '1990-02-19T20:11+02:00', 'dow': ['WE', 'TH', 'FR'], 'value': 0}}
    assert dict(scheduler._persistent_data()) == expected


@pytest.mark.asyncio
async def test_scheduler_is_clean_after_construction_from_persistent_data(scheduler: CustomScheduler):
    rec_obj = RecordContainer({
        'pkey': 'salum',
        'target': 'L4',
        'start_at': '1990-02-19T08:09+02:00',
        'end_at': '1990-02-19T20:14+02:00',
        'dow': ['TH', 'FR', 'SA'],
        'value': 50,
    })
    fd = BytesIO()
    scheduler.add_double_job(rec_obj)
    await scheduler.persist(fd)
    scheduler.shutdown()  # free aby resources, etc.
    scheduler.instance = None  # cleanup before creating a new instance
    CustomScheduler.persistent_file = fd
    loaded_scheduler = await CustomScheduler.from_persistent_data()
    assert loaded_scheduler.is_dirty() is False


@pytest.mark.asyncio
async def test_minimal_full_cycle_scenario(scheduler: CustomScheduler):
    rec_obj = RecordContainer({
        'pkey': 'samar',
        'target': 'P4',
        'start_at': '1990-02-19T08:07+02:00',
        'end_at': '1990-02-19T20:12+02:00',
        'dow': ['TH', 'FR'],
        'value': 50
    })
    scheduler.__class__.persistent_file = BytesIO()
    scheduler.add_double_job(rec_obj)
    initial_data = scheduler._persistent_data().copy()
    await scheduler.persist()
    # no need to kill the instance in CustomScheduler.instance as it was not yet set
    recreated = await CustomScheduler.from_persistent_data()
    expected = {'samar': {'pkey': 'samar', 'target': 'P4', 'start_at': '1990-02-19T08:07+02:00',
                          'end_at': '1990-02-19T20:12+02:00', 'dow': ['TH', 'FR'], 'value': 50}}
    assert initial_data == expected
    assert recreated._persistent_data() == initial_data


def test_scheduler_is_dirty_after_put(scheduler: CustomScheduler):
    assert scheduler.is_dirty() is False
    rec_obj = RecordContainer({
        'pkey': 'elemse',
        'target': 'P1',
        'start_at': '1990-02-19T01:02+02:00',
        'end_at': '1990-02-19T02:03+02:00',
        'dow': ['TH', 'FR'],
        'value': 100
    })
    scheduler.add_double_job(rec_obj)
    assert scheduler.is_dirty() is True


def test_scheduler_is_dirty_after_delete(scheduler: CustomScheduler):
    assert scheduler.is_dirty() is False
    rec_obj = RecordContainer({
        'pkey': 'elemse2',
        'target': 'P1',
        'start_at': '1990-02-19T01:02+02:00',
        'end_at': '1990-02-19T02:03+02:00',
        'dow': ['TH', 'FR'],
        'value': 100
    })
    scheduler.add_double_job(rec_obj)
    scheduler.set_clean()
    assert scheduler.is_dirty() is False
    scheduler.remove_double_job('elemse2')
    assert scheduler.is_dirty() is True




