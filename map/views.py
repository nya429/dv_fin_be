import json
import uuid

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Max, Count
from map.models import (Tracker, Location, Setting)
from .serializers import (LocationSerializer, TrackerSerializer)
from map import serializers

# Create your views here.
limit = 15

@api_view(['GET'])
def test(request):
    # data = json.loads(request.body)
    response = {"Success": False}
    try:

        tracker_top10 = Location.objects.all()[:10]
        serializer = LocationSerializer(tracker_top10, many=True)

        response["data"] = serializer.data
        response["Success"] = True

        return Response(response)
    except Exception as e:
        return Response(response)


@api_view(['GET'])
def getLastActive(request):
    # data = json.loads(request.body)
    response = {"Success": False}

    try:
        query = Location.objects \
            .values('tracker_id') \
            .annotate(max_time=Max('time'))[:limit] \

        serializer = LocationSerializer(query, many=True)

        response["data"] = serializer.data
        response["Success"] = True

        return Response(response)
    except Exception as e:
        return Response(response)


@api_view(['POST'])
def getLocationBySpan(request):
    data = json.loads(request.body)
    tracker_id = data['tracker_id']
    # tracker_id = 'c60'

    response = {"Success": False}

    try:
        query = Location.objects \
            .filter(tracker_id=tracker_id)[:300]

        serializer = LocationSerializer(query, many=True)

        response["data"] = serializer.data
        response["Success"] = True

        return Response(response)
    except Exception as e:
        return Response(response)
