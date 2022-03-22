from rest_framework import serializers
from rest_framework.fields import empty
from .models import Location, Tracker, Setting


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('__all__')

    def __init__(self, instance=None, data=empty, **kwargs):
        super(LocationSerializer, self).__init__(instance, data, **kwargs)
        if instance is not None and instance._fields is not None:
            allowed = set(instance._fields)
            existing = set(self.fields.keys())
            for fn in existing - allowed:
                self.fields.pop(fn)


class TrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracker
        fields = ('tracker_id')
