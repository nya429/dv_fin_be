import json
import uuid

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Max, Count
from map.models import (Tracker, Location, Setting)
from .serializers import (LocationSerializer, TrackerSerializer)
from map import serializers
import datetime
import time

# Create your views here.
limit = 15

@api_view(['GET'])
def test(request):
    # data = json.loads(request.body)
    response = {"Success": False}
    try:

        tracker_top10 = Location.objects.all()[:3]
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
            .filter(tracker_id=tracker_id)[:60]

        serializer = LocationSerializer(query, many=True)

        response["data"] = serializer.data
        response["Success"] = True

        return Response(response)
    except Exception as e:
        return Response(response)



def heart_beat(data=''):
    while True:
        time.sleep(1)
        yield f'sys_time: {datetime.datetime.now()}, {data}\n'


def stream_event(time_limit=5):
    trackers = Location.objects \
        .values('tracker_id') \
        .annotate(max_time=Max('time'))[:limit] 
    tracker_ids = [t['tracker_id'] for t in trackers]

    query = Location.objects \
        .values('time')[:time_limit] 

    time_idx = 0
    time_len = len(query)
    while True:
        time.sleep(3)
        if time_idx == time_len:
            time_idx = 0

        time_stamp = query[time_idx]['time']
        time_locations = Location.objects.filter(time=time_stamp, tracker_id__in=tracker_ids)\
            .values('tracker_id', 'loc_x', 'loc_y', 'time')
        time_locations_data = LocationSerializer(time_locations, many=True).data
        
        time_idx += 1
        
        yield f'tracker_locations: {time_locations_data}\n\n'


@api_view(['GET'])
def sse_test(request):
    return StreamingHttpResponse(heart_beat(), content_type='text/event-stream')


@api_view(['GET'])
def sse(request):
    return StreamingHttpResponse(stream_event(), content_type='text/event-stream')