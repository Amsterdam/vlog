from django.db import models


class VehicleCategory(models.Model):
    """
    A category for vehicles, e.g. auto, aanhanger, motor.
    Note that this could also be a vehicle code, such as 'M1'.
    """

    name = models.CharField(max_length=255, unique=True)


class Publication(models.Model):
    """
    A data publication posted to our api which contains Measurements for
    MeasurementSites.
    """

    type = models.CharField(
        max_length=255,
        help_text=(
            "The type of publication. One of: TrafficFlow, TravelTime, "
            "IndividualTravelTime"
        ),
    )
    reference_id = models.CharField(
        max_length=255,
        help_text=(
            "Unique publication identifier. The ID is a unique for data set delivered "
            "by the system and shall remain unchanged throughout the system lifetime"
        ),
    )
    version = models.CharField(
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
    measurement_duration = models.IntegerField(
        null=True,
        help_text=(
            "The duration element provides the measurement frequency at which "
            "the travel time values are calculated/exported."
        ),
    )


class Measurement(models.Model):
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    measurement_site_reference_id = models.CharField(max_length=255)  # e.g. "SEC_0001"
    measurement_site_reference_version = models.CharField(max_length=255)  # e.g. "1.0"
    measurement_site_name = models.CharField(max_length=255, null=True)
    measurement_site_type = models.CharField(max_length=255)  # e.g. "section"
    length = models.IntegerField(null=True)


class Location(models.Model):
    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)
    index = models.IntegerField(null=True)  # e.g. 1, 2, 3, 4


class Lane(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    specific_lane = models.CharField(
        max_length=255
    )  # Sometimes an int, sometimes a string. Because why not?
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
    type = models.CharField(
        max_length=255,
        help_text=("One of: raw, representative, processed, predicted, actual"),
    )
    num_input_values_used = models.IntegerField(
        null=True,
        help_text=(
            "The total no: of samples (individual travel times) used to "
            "compute the travel time."
        ),
    )
    estimation_type = models.CharField(
        max_length=255,
        null=True,
        help_text=(
            "The type of estimation used, one of best, estimated, instantaneous, "
            "reconstituted"
        ),
    )
    data_quality = models.FloatField(
        null=True, help_text=("Quality of the computed travel time/speed (0...100%)")
    )
    data_error = models.BooleanField(
        max_length=255,
        default=False,
        help_text=(
            "Optional elemnt to indicate whether there were errors in the "
            "travel time computation or there are alarm reported against this site."
        ),
    )
    travel_time = models.IntegerField(
        help_text=("The computed travel time in seconds.")
    )
    traffic_speed = models.IntegerField(
        help_text=("The computed driving speed in kmph.")
    )


class IndividualTravelTime(models.Model):
    # <individualTravelTimeData>
    #     <licensePlate>ABCDEFGHIJKLMNOPQRSTUVWXYZ11111111111111</licensePlate>
    #     <vehicleCategory>M1</vehicleCategory>
    #     <startDetectionTime>2019-01-22T11:55:12Z</startDetectionTime>
    #     <endDetectionTime>2019-01-22T11:55:18Z</endDetectionTime>
    #     <travelTime>6</travelTime>
    #     <trafficSpeed>300</trafficSpeed>
    # </individualTravelTimeData>
    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=255)
    vehicle_category = models.CharField(max_length=255)
    start_detection_time = models.DateTimeField()
    end_detection_time = models.DateTimeField()
    travel_time = models.IntegerField()
    traffic_speed = models.IntegerField()


class MeasuredFlow(models.Model):
    # <measuredFlow specificLane="lane1">
    #     <vehicleFlow>6</vehicleFlow>
    #     <numberOfInputValuesUsed>
    #         <category count="6" type="Auto" />
    #     </numberOfInputValuesUsed>
    # </measuredFlow>
    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)
    specific_lane = models.CharField(max_length=255)
    vehicle_flow = models.IntegerField()


class Category(models.Model):
    measured_flow = models.ForeignKey('MeasuredFlow', on_delete=models.CASCADE)
    count = models.IntegerField()
    type = models.CharField(max_length=255, null=True)
