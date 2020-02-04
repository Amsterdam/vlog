import pytest
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from rest_framework import status

from vlog.models import Vlog


@pytest.mark.django_db
class TestLineTestCase:
    @pytest.mark.parametrize(
        "data, row_count", [
            pytest.param(
                [("2020-1-23 00:00", "6", "0600A10500")],
                1,
            ),
            ((("2020-01-23 00:00:03.521", "10", "0A0281010465"), ), 1),
            ((
                ("2020-01-23 00:00:00.399", "6", "0600A10500"),
                ("2020-01-23 00:00:02.220", "10", "0A0171010063"),
                ("2020-01-23 00:00:02.941", "10", "0A06120C0060160061"),
                ("2020-01-23 00:00:03.521", "10", "0A0281010465"),
            ), 4),
            ((
                ("2020-01-23 00:00:00.399", "6", "0600A10500"),
                ("  "),
                ("  ", "0", "0600A10500"),
                ("  2020-01-23 00:00:02.941", "10", "0A0171010064  "),
                ("2020-01-23 00:00:03.521  ", " 10 ", " 0A0281010465 "),
            ), 3),
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
        body_lines = [','.join(x) for x in data]
        body = '\n'.join(body_lines)
        response = api_client.post(url, body, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Vlog.objects.count() == row_count

        # Validate the database
        for i, log in enumerate(data):
            if not log[0].strip():
                continue
            row = Vlog.objects.get(vri_id=101, time=log[0].strip())
            assert row.vri_id == 101
            assert row.message_type == int(log[1])
            assert row.message == log[2].strip()

    def test_list_vlog_not_allowed(self, api_client):
        url = reverse('api:vlog-list', kwargs={'version': 'v1'})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_vlog_not_allowed(self, api_client):
        url = reverse('api:vlog-list', kwargs={'version': 'v1'})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_patch_vlog_not_allowed(self, api_client):
        url = reverse('api:vlog-list', kwargs={'version': 'v1'})
        response = api_client.patch(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_detail_does_not_exist(self):
        with pytest.raises(NoReverseMatch):
            reverse('api:vlog-detail', kwargs={'pk': 1})
