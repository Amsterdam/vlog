from django.test import TestCase
import logging

import pytz
from .models import VlogRecord
from .consumer import save_line

log = logging.getLogger(__name__)
timezone = pytz.timezone("Europe/Amsterdam")


class LineTestCase(TestCase):
    def setUp(self):
        self.test_records = """2019-12-10 15:17:00 448,331,0647611B00
            2019-12-10 15:17:00 183,678,0644A22D001F01
            2019-12-10 15:17:00 214,865,0A42D1310027
            2019-12-10 15:17:00 277,461,1044E24D20
            2019-12-10 15:17:00 323,403,0E44115701
            2019-12-10 15:17:00 698,403,0644216C01
            2019-12-10 15:17:00 730,403,0665211901
            2019-12-10 15:17:00 761,403,0644324A00"""

    def test_vanilla_line_input(self):
        for line in self.test_records.split("\n"):
            record = save_line(line)
            self.assertEqual(type(record), VlogRecord)
            self.assertEqual(record.vri_id, int(line.split(',')[1].strip()))
        self.assertEqual(VlogRecord.objects.count(), len(self.test_records.split("\n")))

    def test_missing_raw_value(self):
        self.assertRaises(ValueError, save_line, '2019-12-10 15:17:00 214,865')
        self.assertEqual(VlogRecord.objects.count(), 0)

    def test_empty_raw_value(self):
        self.assertRaises(ValueError, save_line, '2019-12-10 15:17:00 214,865,')
        self.assertEqual(VlogRecord.objects.count(), 0)

    def test_malformed_recorded_at(self):
        self.assertRaises(ValueError, save_line, '2019-12-10 15:1700 698,403,0644216C01')
        self.assertEqual(VlogRecord.objects.count(), 0)

    def test_empty_vri_id(self):
        self.assertRaises(ValueError, save_line, '2019-12-10 15:1700 698,,0644216C01')
        self.assertEqual(VlogRecord.objects.count(), 0)
