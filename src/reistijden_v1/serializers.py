from rest_framework import serializers

from reistijden_v1.models import (
    IndividualTravelTime,
    Lane,
    Measurement,
    MeasurementLocation,
    MeasurementSite,
    Publication,
    TrafficFlow,
    TrafficFlowCategoryCount,
    TravelTime,
)


class LaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lane
        exclude = ['measurement_location']


class MeasurementLocationSerializer(serializers.ModelSerializer):
    lanes = LaneSerializer(many=True)

    class Meta:
        model = MeasurementLocation
        exclude = ['measurement_site']


class TravelTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelTime
        exclude = ['measurement']


class IndividualTravelTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualTravelTime
        exclude = ['measurement']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFlowCategoryCount
        exclude = ['traffic_flow']


class TrafficFlowSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = TrafficFlow
        exclude = ['measurement']


class MeasurementSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementSite
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    measurement_site = MeasurementSiteSerializer(many=False)
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
            measurement_site_src = measurement_src.pop('measurement_site')
            measurement_site, _ = MeasurementSite.objects.get_or_create(
                **measurement_site_src
            )

            measurement = Measurement.objects.create(
                publication=publication, measurement_site=measurement_site
            )

            locations = measurement_src.pop('locations')
            travel_times = measurement_src.pop('travel_times')
            individual_travel_times = measurement_src.pop('individual_travel_times')
            traffic_flows = measurement_src.pop('traffic_flows')

            for location_src in locations:
                lanes = location_src.pop('lanes')
                measurement_location, _ = MeasurementLocation.objects.get_or_create(
                    measurement_site=measurement_site, **location_src
                )

                for lane_src in lanes:
                    Lane.objects.create(measurement_location=measurement_location, **lane_src)

            for travel_time_src in travel_times:
                TravelTime.objects.create(measurement=measurement, **travel_time_src)

            for individual_travel_time_src in individual_travel_times:
                IndividualTravelTime.objects.create(
                    measurement=measurement, **individual_travel_time_src
                )

            for traffic_flow_src in traffic_flows:
                categories = traffic_flow_src.pop('categories')
                traffic_flow = TrafficFlow.objects.create(
                    measurement=measurement, **traffic_flow_src
                )

                for category_src in categories:
                    TrafficFlowCategoryCount.objects.create(
                        traffic_flow=traffic_flow, **category_src
                    )

        return publication
