from rest_framework import serializers

from .models import (IndividualTravelTime, Location, Measurement, Publication,
                     TrafficFlow, TravelTime)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ['measurement']


class TravelTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelTime
        exclude = ['measurement']


class IndividualTravelTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualTravelTime
        exclude = ['measurement']


class TrafficFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrafficFlow
        exclude = ['measurement']


class MeasurementSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
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

        for site_measurement in measurements:
            locations = site_measurement.pop('locations')
            travel_times = site_measurement.pop('travel_times')
            individual_travel_times = site_measurement.pop('individual_travel_times')
            traffic_flows = site_measurement.pop('traffic_flows')

            measurement = Measurement.objects.create(
                publication=publication,
                **site_measurement
            )

            for location in locations:
                Location.objects.create(
                    measurement=measurement,
                    **location
                )

            for travel_time in travel_times:
                TravelTime.objects.create(
                    measurement=measurement,
                    **travel_time
                )

            for individual_travel_time in individual_travel_times:
                IndividualTravelTime.objects.create(
                    measurement=measurement,
                    **individual_travel_time
                )

            for traffic_flow in traffic_flows:
                TrafficFlow.objects.create(
                    measurement=measurement,
                    **traffic_flow
                )

        return publication
