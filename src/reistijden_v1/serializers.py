from rest_framework import serializers

from reistijden_v1.models import (
    IndividualTravelTime,
    Lane,
    Measurement,
    MeasurementLocation,
    Publication,
    TrafficFlow,
    TrafficFlowCategoryCount,
    TravelTime,
    VehicleCategory,
)


class LaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lane
        exclude = ['measurement_location']


class MeasurementLocationSerializer(serializers.ModelSerializer):
    lanes = LaneSerializer(many=True)

    class Meta:
        model = MeasurementLocation
        exclude = ['measurement']


class TravelTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelTime
        exclude = ['measurement']


class IndividualTravelTimeSerializer(serializers.ModelSerializer):
    vehicle_category = serializers.CharField(max_length=255, allow_null=True)

    class Meta:
        model = IndividualTravelTime
        exclude = ['measurement']


class TrafficFlowCategoryCountSerializer(serializers.ModelSerializer):
    vehicle_category = serializers.CharField(max_length=255, allow_null=True)

    class Meta:
        model = TrafficFlowCategoryCount
        exclude = ['traffic_flow']


class TrafficFlowSerializer(serializers.ModelSerializer):
    traffic_flow_category_counts = TrafficFlowCategoryCountSerializer(many=True)

    class Meta:
        model = TrafficFlow
        exclude = ['measurement']


class MeasurementSerializer(serializers.ModelSerializer):
    locations = MeasurementLocationSerializer(many=True)
    travel_times = TravelTimeSerializer(many=True)
    individual_travel_times = IndividualTravelTimeSerializer(many=True)
    traffic_flows = TrafficFlowSerializer(many=True)

    class Meta:
        model = Measurement
        exclude = ['publication']


class PublicationSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Publication
        fields = "__all__"

    def create(self, validated_data):
        measurements = validated_data.pop('measurements')
        publication = Publication.objects.create(**validated_data)

        for measurement_src in measurements:
            locations = measurement_src.pop('locations')
            travel_times = measurement_src.pop('travel_times')
            individual_travel_times = measurement_src.pop('individual_travel_times')
            traffic_flows = measurement_src.pop('traffic_flows')

            measurement = Measurement.objects.create(
                publication=publication, **measurement_src
            )

            for location_src in locations:
                lanes = location_src.pop('lanes')
                measurement_location = MeasurementLocation.objects.create(
                    measurement=measurement, **location_src
                )

                for lane_src in lanes:
                    Lane.objects.create(
                        measurement_location=measurement_location, **lane_src
                    )

            for travel_time_src in travel_times:
                TravelTime.objects.create(measurement=measurement, **travel_time_src)

            for individual_travel_time_src in individual_travel_times:
                (
                    individual_travel_time_src['vehicle_category'],
                    _,
                ) = VehicleCategory.get_or_create(
                    individual_travel_time_src['vehicle_category']
                )
                IndividualTravelTime.objects.create(
                    measurement=measurement, **individual_travel_time_src
                )

            for traffic_flow_src in traffic_flows:
                traffic_flow_category_counts = traffic_flow_src.pop(
                    'traffic_flow_category_counts'
                )
                traffic_flow = TrafficFlow.objects.create(
                    measurement=measurement, **traffic_flow_src
                )

                for traffic_flow_category_count_src in traffic_flow_category_counts:
                    (
                        traffic_flow_category_count_src['vehicle_category'],
                        _,
                    ) = VehicleCategory.get_or_create(
                        traffic_flow_category_count_src['vehicle_category']
                    )
                    TrafficFlowCategoryCount.objects.create(
                        traffic_flow=traffic_flow, **traffic_flow_category_count_src
                    )

        return publication
