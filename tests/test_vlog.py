import pytest
from django.urls import reverse
from rest_framework import status

from vlog.models import Vlog
from vlog.parsers import parse_vlog_line


@pytest.mark.django_db
class TestLineTestCase:
    @pytest.mark.parametrize(
        "data, row_count", [
            pytest.param(
                [
                    ("2020-1-23 00:00,101,6,0600A10500"),
                ],
                1,
            ),
            pytest.param(
                [
                    (" 2020-01-23 00:00:03.521 , 101,10, 0A0281010465 "),
                ],
                1,
            ),
            pytest.param(
                [
                    ("2020-01-23 00:00:00.399 ,101, 6, 0600A10500"),
                    ("2020-01-23 00:00:02.220,102 ,10,0A0171010063"),
                    ("2020-01-23 00:00:02.941, 103,10,0A06120C0060160061"),
                    ("2020-01-23 00:00:03.521, 101 , 10, 0A0281010465"),
                ],
                4,
            ),
            pytest.param(
                [
                    ("2020-01-23 00:00:00.399, 101,6,0600A10500"),
                    ("2020-01-23 00:00:02.941,102 ,10,0A0171010064  "),
                    ("2020-01-23 00:00:03.521,103, 10 ,0A0281010465 "),
                ],
                3,
            ),
        ]
    )
    def test_create_vlog_bulk(
        self, django_assert_num_queries, api_client, data, row_count
    ):
        """
        Ensure we can create new objects
        """
        url = reverse('api:vlog-list', kwargs={'version': 'v1'})

        # Validate the insert was in bulk
        body = '\n'.join(data)
        with django_assert_num_queries(1):
            response = api_client.post(url, body, format='txt')

        assert response.status_code == status.HTTP_201_CREATED
        assert Vlog.objects.count() == row_count

        # Validate the database
        for i, line in enumerate(data):
            vlog = parse_vlog_line(line)
            row = Vlog.objects.get(vri_id=vlog['vri_id'], time=vlog['time'])
            assert row.vri_id == vlog['vri_id']
            assert row.message_type == vlog['message_type']
            assert row.message == vlog['message']

    def test_list_vlog(self, api_client):
        url = reverse('api:vlog-list', kwargs={'version': 'v1'})
        api_client.get(url, format='txt')
