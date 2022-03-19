from rest_framework import serializers
from .models import Location, Tracker, Setting

class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = ('tracker_id', 'time', 'loc_x', 'loc_y')


class TrackerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tracker
        fields = ('tracker_id')