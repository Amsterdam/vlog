from django.db import models


class Publication(models.Model):
    """
    A data publication posted to our api which contains Measurements for
    MeasurementSites.
    """

    publication_type = models.CharField(
        max_length=255,
        help_text=(
            "The type of publication. One of: TrafficFlow, TravelTime, "
            "IndividualTravelTime"
        ),
    )
    publication_reference_id = models.CharField(
        max_length=255,
        help_text=(
            "Unique publication identifier. The ID is a unique for data set delivered "
            "by the system and shall remain unchanged throughout the system lifetime"
        ),
    )
    publication_reference_version = models.CharField(
        max_length=255,
        help_text=(
            "The version of the publication. Incremented (+1) every time section "
            "and/or route definition are modified i.e., a) New section(s) and/or "
            "trajectory(ies) are activated, b) Existing section(s) and/or "
            "trajectory(ies) are deactivated c)	Existing section(s) and/or "
            "trajectories are modified"
        ),
    )
    publication_time = models.DateTimeField(
        help_text=(
            "The date time the latest version (refer attribute 'version') "
            "for this publication was published in UTC format: ISO 8601 "
            "[https://en.wikipedia.org/wiki/ISO_8601]"
        )
    )

    # The following defines the period against which the statistics were reported.
    # The period is defined either using the measurementStartTime-duration pair
    # or measurementStartTime-measurementendTime pair.
    # A default measurement period of 60s is assumed, if duration and
    # measurementEndTime elements are not present.
    measurement_start_time = models.DateTimeField(
        help_text=(
            "The time recorded here is the starting time of the supply period "
            "in UTC format: ISO 8601 [https://en.wikipedia.org/wiki/ISO_8601]"
        )
    )
    measurement_end_time = models.DateTimeField(
        null=True,
        help_text=(
            "The time recorded here is the ending time of the supply period "
            "in UTC format: ISO 8601 [https://en.wikipedia.org/wiki/ISO_8601]"
        ),
    )


class Measurement(models.Model):
    """
    A measurement for a specific MeasurementSite, published in a Publication.
    """
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    measurement_site_reference_id = models.CharField(max_length=255)  # e.g. "SEC_0001"
    measurement_site_reference_version = models.CharField(max_length=255)  # e.g. "1.0"
    measurement_site_name = models.CharField(max_length=255, null=True)
    measurement_site_type = models.CharField(max_length=255)  # e.g. "section"
    length = models.IntegerField(null=True)


class Location(models.Model):
    """
    A location that is part of the MeasurementSite.
    At most one location exists if the measurement site is of type 'location.
    A maximum of two locations should be present if the measurement site is of type
    'section' (start and end location).
    The number of locations is unbounded if the measurement site is of type
    'trajectory' (start location, end location and all via locations)
    """
    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)

    index = models.IntegerField(
        null=True,
        help_text=(
            "The index attribute indicates the order of measurement location in the "
            "measurement site. Optional, if the measurement site is of type 'location'"
        ),
    )


class Lane(models.Model):
    """
    A road lane at a Location.
    """

    location = models.ForeignKey(
        'Location', on_delete=models.CASCADE
    )
    specific_lane = models.CharField(
        max_length=255,
        help_text=(
            "Indicative name for the lane (lane1, lane2, lane3 … lane9 etc) "
            "Indicative name for the lane (lane1, lane2, lane3 … lane9 etc) "
            "used in the Amsterdam Travel Time system. The actual lane number is "
            "available at Camera.lane_number with respect to the camera view direction "
            "at the measurement location."
        ),
    )
    camera_id = models.CharField(max_length=255)  # Are either UUIDs OR ints in strings
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Decimal(9,6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Decimal(9,6)
    lane_number = models.IntegerField()  # e.g. 1, 2, 3, 4
    status = models.CharField(max_length=255)  # e.g. "on"
    view_direction = models.IntegerField()  # e.g. 225


class TravelTime(models.Model):
    """
    A Measurement measured over multiple MeasurementLocations which contains
    the general travel time and traffic speed for traffic passing these locations.
    """

    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)
    travel_time_type = models.CharField(
        max_length=255,
        help_text=("One of: raw, representative, processed, predicted, actual"),
    )
    data_quality = models.FloatField(
        null=True, help_text=("Quality of the computed travel time/speed (0...100%)")
    )
    estimation_type = models.CharField(
        max_length=255,
        null=True,
        help_text=(
            "The type of estimation used, one of best, estimated, instantaneous, "
            "reconstituted"
        ),
    )
    travel_time = models.IntegerField(
        help_text=("The computed travel time in seconds.")
    )
    traffic_speed = models.IntegerField(
        help_text=("The computed driving speed in kmph.")
    )


class IndividualTravelTime(models.Model):
    """
    A Measurement measured over multiple MeasurementLocations which contains
    the specific travel time and traffic stpeed for a single vehicle.
    """

    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=255)
    vehicle_category = models.CharField(max_length=255)
    start_detection_time = models.DateTimeField(
        help_text=(
            "The date time the vehicle was detected at the start location of the "
            "measurement site (section) in UTC format."
        ),
        null=True,
        blank=True,
    )
    end_detection_time = models.DateTimeField(
        help_text=(
            "The date time the vehicle was detected at the end lcoation of the "
            "measurement site (section) in UTC format."
        ),
        null=True,
        blank=True,
    )
    travel_time = models.IntegerField(
        help_text=("The computed travel time in seconds.")
    )
    traffic_speed = models.IntegerField(
        help_text=("The computed driving speed in kmph.")
    )


class MeasuredFlow(models.Model):
    """
    MeasuredFlow describes the intensity data computed for a specific lane
    in the measurement location.
    """

    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)
    specific_lane = models.CharField(
        max_length=255,
        help_text=(
            "Indicative name for the lane (lane1, lane2, lane3 … lane9 etc) used in "
            "the Amsterdam Travel Time system. See Lane.specific_lane."
        ),
    )
    vehicle_flow = models.IntegerField(
        help_text=(
            "Provides the total number of vehicle detections at the "
            "measurement site (location) for the measurement period."
        )
    )


class Category(models.Model):
    measured_flow = models.ForeignKey('MeasuredFlow', on_delete=models.CASCADE)
    count = models.IntegerField()
    type = models.CharField(max_length=255, null=True)
