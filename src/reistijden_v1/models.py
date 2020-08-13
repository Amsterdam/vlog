from django.db import models


class Publication(models.Model):
    publication_type = models.CharField(max_length=255)  # one of travelTime or trafficFlow
    publication_reference_id = models.CharField(max_length=255)  # e.g. PUB_AMS_ACTUAL_TRAJECTORY_TT
    publication_reference_version = models.CharField(max_length=255)  # e.g. "1.0"
    publication_time = models.DateTimeField()
    measurement_start_time = models.DateTimeField()
    measurement_end_time = models.DateTimeField()


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
    specific_lane = models.CharField(max_length=255)  # Sometimes an int, sometimes a string. Because why not?
    camera_id = models.CharField(max_length=255)  # Are either UUIDs OR ints in strings
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Decimal(9,6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Decimal(9,6)
    lane_number = models.IntegerField()  # e.g. 1, 2, 3, 4
    status = models.CharField(max_length=255)  # e.g. "on"
    view_direction = models.IntegerField()  # e.g. 225


class TravelTime(models.Model):
    # <travelTimeData travelTimeType="predicted" estimationType="estimated">
    #     <travelTime>73</travelTime>
    #     <trafficSpeed>50</trafficSpeed>
    # </travelTimeData>
    measurement = models.ForeignKey('Measurement', on_delete=models.CASCADE)
    travel_time_type = models.CharField(max_length=255)
    data_quality = models.FloatField(null=True)
    estimation_type = models.CharField(max_length=255, null=True)
    travel_time = models.IntegerField()
    traffic_speed = models.IntegerField()


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
