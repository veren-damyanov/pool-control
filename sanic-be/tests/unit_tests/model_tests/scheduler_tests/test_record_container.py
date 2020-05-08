"""Unit tests for the RecordContainer class."""
import pytest

from poolctl.model.scheduler.record_container import RecordContainer


class TestRecordContainer:

    def test__dow_as_day_of_week_arg__lowercase(self):
        dow_record = {
            'dow': ['we', 'fr', 'su'],
            'value': 0
        }
        result = RecordContainer._dow_as_day_of_week_arg(dow_record)
        assert result == '2,4,6'

    def test__dow_as_day_of_week_arg__uppercase__shuffled(self):
        dow_record = {
            'dow': ['su', 'sa', 'we', 'fr'],
            'value': 0
        }
        result = RecordContainer._dow_as_day_of_week_arg(dow_record)
        assert result == '2,4,5,6'

    def test_wishful_api(self):
        rec_obj = RecordContainer({
            'pkey': 'gyroje',
            'target': 'T',
            'start_at': '1990-02-19T08:05+02:00',
            'end_at': '1990-02-19T20:10+02:00',
            'dow': ['MO', 'TU', 'WE', 'TH', 'FR'],
            'value': 0
        })
        assert rec_obj.id == 'gyroje'
        assert rec_obj.target == 'T'
        assert rec_obj.start_at == '1990-02-19T08:05+02:00'
        assert rec_obj.end_at == '1990-02-19T20:10+02:00'
        assert rec_obj.start_at_hour_minute() == (8, 5)
        assert rec_obj.end_at_hour_minute() == (20, 10)
        assert rec_obj.dow == '0,1,2,3,4'
        assert rec_obj.timing == '08:05 - 20:10'
