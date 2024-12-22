from rest_framework import serializers
from .models import Itinerary, Day, Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'name', 'time']

class DaySerializer(serializers.ModelSerializer):
    destinations = DestinationSerializer(many=True, read_only=True)

    class Meta:
        model = Day
        fields = ['id', 'day_number', 'date', 'destinations']

class ItinerarySerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = ['id', 'name', 'cover', 'days']
