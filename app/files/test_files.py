from django.test import TestCase, Client
import logging

import pytz

from .models import VlogRecord

log = logging.getLogger(__name__)
timezone = pytz.timezone("UTC")


class FileTestCase(TestCase):
    def setUp(self):
        self.url = '/files/'
        self.c = Client()
        self.test_data = "a\nb  \n c\n\n"  # dirty test string with some spaces and empty lines

    def test_post(self):
        """ Test posting a new file """
        response = self.c.post(self.url, self.test_data, content_type="text/plain")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VlogRecord.objects.count(), len([x.strip() for x in self.test_data.split("\n") if x.strip()]))
        posted_strings = [x.strip() for x in self.test_data.split("\n")]
        for record in VlogRecord.objects.all():
            self.assertIn(record.raw, posted_strings)

    def test_get_not_allowed(self):
        """ Test whether the api correctly returns a not allowed error for get """
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_put_not_allowed(self):
        """ Test whether the api correctly returns a not allowed error for put """
        response = self.c.put(self.url)
        self.assertEqual(response.status_code, 405)

    def test_delete_not_allowed(self):
        """ Test whether the api correctly returns a not allowed error for delete """
        response = self.c.delete(self.url)
        self.assertEqual(response.status_code, 405)

    def test_patch_not_allowed(self):
        """ Test whether the api correctly returns a not allowed error for patch """
        response = self.c.patch(self.url)
        self.assertEqual(response.status_code, 405)
