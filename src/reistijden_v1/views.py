import logging
import os
from datetime import datetime
from xml.parsers.expat import ExpatError

import humps
import xmltodict
from rest_framework import exceptions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_xml.parsers import XMLParser

from .serializers import PublicationSerializer

logger = logging.getLogger(__name__)


def store_error_content(e, request):
    """
    In order to keep the content of the messages that resulted in errors, we store them in the container for now.
    This is a massive hack and should be removed very soon. If you find this code, please remove it.
    """
    try:
        error_type = e.__repr__().replace("'", '')
        folder = '/tmp/errors/'
        file_path = f'{folder}{datetime.now().isoformat()}-{error_type}.xml'
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(file_path, 'w') as f:
            f.write(request.body.decode("utf-8"))
    except Exception as e:
        logger.error(e)


def location_src_to_dict(src_d):
    return {
        'index': src_d.get('@index'),
        'specific_lane': src_d['lane']['@specific_lane'],
        'camera_id': src_d['lane']['camera']['@id'],
        'latitude': src_d['lane']['camera']['coordinates']['@latitude'],
        'longitude': src_d['lane']['camera']['coordinates']['@longitude'],
        'lane_number': src_d['lane']['camera']['lane_number'],
        'status': src_d['lane']['camera']['status'],
        'view_direction': src_d['lane']['camera']['view_direction'],
    }


def travel_time_src_to_dict(src_d):
    return {
        'travel_time_type': src_d['@travel_time_type'],
        'estimation_type': src_d['@estimation_type'],
        'travel_time': src_d['travel_time'],
        'traffic_speed': src_d['traffic_speed'],
    }


def traffic_flow_src_to_dict(src_d):
    measured_flow = src_d['measured_flow']
    return {
        'specific_lane': measured_flow['@specific_lane'],
        'vehicle_flow': measured_flow['vehicle_flow'],
        'category_count': measured_flow['number_of_input_values_used']['category']['@count'],
        'category_type': measured_flow['number_of_input_values_used']['category']['@type'],
    }


def get_location_from_site_ref(site_ref):
    if 'location' in site_ref:
        return [location_src_to_dict(site_ref['location'])]
    else:
        return [location_src_to_dict(d) for d in site_ref['location_contained_in_itinerary']['location']]


def measurement_src_to_dict(src_d):
    site_ref = src_d['measurement_site_reference']
    return {
        'measurement_site_reference_id': site_ref['@id'],
        'measurement_site_reference_version': site_ref['@version'],
        'measurement_site_name': site_ref.get('measurement_site_name'),
        'measurement_site_type': site_ref['measurement_site_type'],
        'length': site_ref.get('length'),
        'locations': get_location_from_site_ref(site_ref),
        'travel_times': [travel_time_src_to_dict(src_d['travel_time_data'])] if 'travel_time_data' in src_d else [],
        'individual_travel_times': [d for d in src_d['individual_travel_time_data']] if 'individual_travel_time_data' in src_d else [],
        'traffic_flows': [traffic_flow_src_to_dict(src_d['traffic_flow_data'])] if 'traffic_flow_data' in src_d else [],
    }


def restructure_data(xml_str):
    data_dict = humps.decamelize(xmltodict.parse(xml_str.strip()))
    publication_src = data_dict['amsterdam_travel_times']['payload_publication']
    return {
        'publication_type': publication_src['@type'],
        'publication_reference_id': publication_src['publication_reference']['@id'],
        'publication_reference_version': publication_src['publication_reference']['@version'],
        'publication_time': publication_src['publication_time'],
        'measurement_start_time': publication_src['measurement_period']['measurement_start_time'],
        'measurement_end_time': publication_src['measurement_period']['measurement_end_time'],
        'measurements': [measurement_src_to_dict(d) for d in publication_src['site_measurements']],
    }


class PublicationViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationSerializer
    serializer_detail_class = PublicationSerializer
    parser_classes = [XMLParser]

    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            restructured_data = restructure_data(request.body.decode("utf-8"))
        except UnicodeError as e:
            logger.error(e)
            store_error_content(e, request)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except (exceptions.ValidationError, KeyError, TypeError) as e:
            logger.error(e)
            store_error_content(e, request)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except ExpatError as e:
            logger.error(e)
            store_error_content(e, request)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        publication_serializer = PublicationSerializer(data=restructured_data)
        publication_serializer.is_valid(raise_exception=True)
        publication_serializer.save()

        return Response("", status=status.HTTP_201_CREATED)
