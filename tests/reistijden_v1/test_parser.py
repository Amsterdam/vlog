import pytest

from src.reistijden_v1.parser import ReistijdenParser


class TestReistijdenParser:
    @pytest.mark.parametrize(
        'data, expected_data',
        [
            (
                {
                    'end_detection_time': 'some_data',
                    'start_detection_time': 'some_data',
                },
                {
                    'detection_end_time': 'some_data',
                    'detection_start_time': 'some_data',
                },
            ),
            (
                {
                    'some_fake_key': 'some_data',
                    'start_detection_time': 'some_data',
                },
                {
                    'detection_start_time': 'some_data',
                    'some_fake_key': 'some_data',
                    'detection_end_time': None,
                },
            ),
            (
                {
                    'end_detection_time': 'some_data',
                    'some_fake_key': 'some_data',
                },
                {
                    'detection_end_time': 'some_data',
                    'detection_start_time': None,
                    'some_fake_key': 'some_data',
                },
            ),
        ],
    )
    def test_convert_detection_key(self, data, expected_data):
        parser = ReistijdenParser('fake_xml')
        response = parser.convert_detection_key(data)
        assert response == expected_data

    @pytest.mark.parametrize(
        'data, expected_data',
        [
            (
                {
                    'individual_travel_time_data': [
                        {
                            'start_detection_time': 'some_data',
                            'end_detection_time': 'some_data',
                        },
                        {
                            'start_detection_time': 'some_data_2',
                            'end_detection_time': 'some_data_2',
                        },
                    ]
                },
                [
                    {
                        'detection_start_time': 'some_data',
                        'detection_end_time': 'some_data',
                    },
                    {
                        'detection_start_time': 'some_data_2',
                        'detection_end_time': 'some_data_2',
                    },
                ],
            ),
            (
                {
                    'individual_travel_time_data': {
                        'start_detection_time': 'some_data',
                        'end_detection_time': 'some_data',
                    }
                },
                [
                    {
                        'detection_start_time': 'some_data',
                        'detection_end_time': 'some_data',
                    }
                ],
            ),
            ({'no_data': {}}, []),
        ],
    )
    def test_get_individual_travel_times_from_measurement(self, data, expected_data):
        parser = ReistijdenParser('fake_xml')

        response = parser.get_individual_travel_times_from_measurement(data)
        assert response == expected_data
