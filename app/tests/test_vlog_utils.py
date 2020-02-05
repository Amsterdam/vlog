import datetime

import pytz
from django.test import override_settings

from vlog.utils import parse_vlog_line, parse_vlog_lines


class TestVlogParser:
    def test_single_line(self):
        line = parse_vlog_line('2020-01-23 14:00:00.399,6,0600A10500')
        assert line['time'].tzinfo == pytz.utc
        assert line['message_type'] == 6
        assert line['message'] == '0600A10500'

    def test_timezone_default(self):
        with override_settings(TIME_ZONE='CET'):
            line = parse_vlog_line('2020-02-23 14:00:00.399,6,0600A10500')
            assert line['time'].isoformat(
            ) == '2020-02-23T13:00:00.399000+00:00'

        with override_settings(TIME_ZONE='UTC'):
            line = parse_vlog_line('2020-02-23 14:00:00.399,6,0600A10500')
            assert line['time'].isoformat(
            ) == '2020-02-23T14:00:00.399000+00:00'

    def test_timezone_utc(self):
        line = parse_vlog_line('2020-02-23 14:00:00.399 UTC,6,0600A10500')
        assert line['time'].isoformat() == '2020-02-23T14:00:00.399000+00:00'

    def test_timezone_cet(self):
        line = parse_vlog_line('2020-02-23T16:00:00.399000+01:00,6,0600A10500')
        assert line['time'].isoformat() == '2020-02-23T15:00:00.399000+00:00'

    def test_timezone_cet_dst(self):
        line = parse_vlog_line('2020-08-23T16:00:00.399000+02:00,6,0600A10500')
        assert line['time'].isoformat() == '2020-08-23T14:00:00.399000+00:00'

    def test_multiple_lines(self):

        dates = (
            "2020-01-23 14:00:00.399",
            "2020-01-24 14:00:02.220",
            "2020-02-23 14:00:02.941",
            "2020-01-24 14:00:03.521",
            "2020-03-23 14:00:03.552",
        )
        types = [6, 10, 333, 595, 9028]
        messages = [
            '0600A10500',
            '0A0171010063',
            '0A0171010064',
            '0A0281010465',
            '2002810110',
        ]

        data = '\n'.join([
            ','.join(map(str, x)) for x in zip(dates, types, messages)
        ])
        lines = parse_vlog_lines(data, strict=True)
        assert len(lines) == 5

        # Assert dates
        for i, val in enumerate(dates):
            assert val.split(' ')[0] in lines[i]['time'].isoformat()

        # Assert types
        for i, val in enumerate(types):
            assert lines[i]['message_type'] == val

        # Assert messages
        for i, val in enumerate(messages):
            assert lines[i]['message'] == val
