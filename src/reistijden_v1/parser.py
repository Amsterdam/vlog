import logging
import os
from datetime import datetime
from distutils.util import strtobool

import humps
import xmltodict

from reistijden_v1.models import VehicleCategory

logger = logging.getLogger(__name__)


class ReistijdenParser:
    def __init__(self, xml_str):
        super().__init__()
        self.xml_str = xml_str

    def restructure_data(self):
        data_dict = humps.decamelize(xmltodict.parse(self.xml_str.strip()))
        publication_src = data_dict["amsterdam_travel_times"]["payload_publication"]

        measurements = []
        if "site_measurements" in publication_src:
            if type(publication_src["site_measurements"]) is list:
                measurements = [
                    self.measurement_src_to_dict(d)
                    for d in publication_src["site_measurements"]
                ]
            else:
                measurements = [
                    self.measurement_src_to_dict(publication_src["site_measurements"])
                ]

        return {
            "type": publication_src["@type"],
            "reference_id": publication_src["publication_reference"]["@id"],
            "version": publication_src["publication_reference"]["@version"],
            "publication_time": publication_src["publication_time"],
            "measurement_start_time": publication_src["measurement_period"][
                "measurement_start_time"
            ],
            "measurement_end_time": publication_src["measurement_period"].get(
                "measurement_end_time"
            ),
            "measurement_duration": publication_src["measurement_period"].get(
                "duration"
            ),
            "measurements": measurements,
        }

    def measurement_src_to_dict(self, src_d):
        site_ref = src_d["measurement_site_reference"]
        return {
            "measurement_site": {
                "reference_id": site_ref["@id"],
                "version": site_ref["@version"],
                "name": site_ref.get("measurement_site_name"),
                "type": site_ref["measurement_site_type"],
                "length": site_ref.get("length"),
            },
            "locations": self.get_location_from_site_ref(site_ref),
            "travel_times": self.get_travel_times_from_measurement(src_d),
            "individual_travel_times": self.get_individual_travel_times_from_measurement(  # noqa: E501
                src_d
            ),
            "measured_flows": self.get_measured_flows_from_measurement(src_d),
        }

    def get_location_from_site_ref(self, site_ref):
        if "location" in site_ref:
            return [self.location_src_to_dict(site_ref["location"])]
        elif "location_contained_in_itinerary" in site_ref:
            return [
                self.location_src_to_dict(d)
                for d in site_ref["location_contained_in_itinerary"]["location"]
            ]
        return []

    def store_error_content(self, e, request):
        """
        In order to keep the content of the messages that resulted in errors,
        we store them in the container for now. This is a massive hack and should
        be removed very soon. If you find this code, please remove it.
        """
        try:
            error_type = e.__repr__().replace("'", "")
            folder = "/tmp/errors/"
            file_path = f"{folder}{datetime.now().isoformat()}-{error_type}.xml"
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(file_path, "w") as f:
                f.write(request.body.decode("utf-8"))
        except Exception as e:
            logger.error(e)

    def lane_src_to_dict(self, src_d):
        return {
            "specific_lane": src_d["@specific_lane"],
            "camera_id": src_d["camera"]["@id"],
            "latitude": src_d["camera"]["coordinates"]["@latitude"],
            "longitude": src_d["camera"]["coordinates"]["@longitude"],
            "lane_number": src_d["camera"]["lane_number"],
            "status": src_d["camera"]["status"],
            "view_direction": src_d["camera"]["view_direction"],
        }

    def location_src_to_dict(self, src_d):
        if type(src_d["lane"]) is list:
            lanes = [self.lane_src_to_dict(lane) for lane in src_d["lane"]]
        else:
            lanes = [self.lane_src_to_dict(src_d["lane"])]

        return {"index": src_d.get("@index"), "lanes": lanes}

    def travel_time_src_to_dict(self, src_d):
        return {
            "type": src_d["@travel_time_type"],
            "data_quality": src_d.get("@data_quality"),
            "estimation_type": src_d.get("@estimation_type"),
            "travel_time": src_d["travel_time"],
            "traffic_speed": src_d["traffic_speed"],
            "num_input_values_used": src_d.get("@number_of_input_values_used"),
            "data_error": bool(strtobool(src_d.get("data_error", "false"))),
        }

    def category_src_to_dict(self, src_d):
        return {
            "count": src_d["@count"],
            "type": src_d["@type"] if src_d["@type"] else None
            # Convert empty strings to Null
        }

    def measured_flow_src_to_dict(self, src_d):
        category_src = src_d["number_of_input_values_used"]["category"]
        if type(category_src) is list:
            categories = [
                self.category_src_to_dict(category) for category in category_src
            ]
        else:
            categories = [self.category_src_to_dict(category_src)]

        return {
            "specific_lane": src_d["@specific_lane"],
            "vehicle_flow": src_d["vehicle_flow"],
            "categories": categories,
        }

    def get_travel_times_from_measurement(self, src_d):
        travel_times = []
        if "travel_time_data" in src_d:
            if type(src_d["travel_time_data"]) is list:
                travel_times = [
                    self.travel_time_src_to_dict(travel_time)
                    for travel_time in src_d["travel_time_data"]
                ]
            else:
                travel_times = [self.travel_time_src_to_dict(src_d["travel_time_data"])]
        return travel_times

    def get_individual_travel_times_from_measurement(self, src_d):
        individual_travel_times = []
        if "individual_travel_time_data" in src_d:
            if type(src_d["individual_travel_time_data"]) is list:
                individual_travel_times = [
                    self.get_individual_travel_time(d)
                    for d in src_d["individual_travel_time_data"]
                ]
            else:
                individual_travel_times = [
                    self.get_individual_travel_time(
                        src_d["individual_travel_time_data"]
                    )
                ]
        return individual_travel_times

    def get_individual_travel_time(self, src_d):
        vehicle_category_str = src_d.pop('vehicle_category')
        if vehicle_category_str:
            vehicle_category, _ = VehicleCategory.objects.get_or_create(
                name=vehicle_category_str
            )
            src_d['vehicle_category'] = vehicle_category.pk

        src_d['detection_start_time'] = src_d.pop('start_detection_time', None)
        src_d['detection_end_time'] = src_d.pop('end_detection_time', None)
        return src_d

    def get_measured_flows_from_measurement(self, src_d):
        measured_flows = []
        if "traffic_flow_data" in src_d:
            measured_flows_src = src_d["traffic_flow_data"]["measured_flow"]
            if type(measured_flows_src) is list:
                measured_flows = [
                    self.measured_flow_src_to_dict(measured_flow)
                    for measured_flow in measured_flows_src
                ]
            else:
                measured_flows = [self.measured_flow_src_to_dict(measured_flows_src)]
        return measured_flows
