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

"""
corners: TL, TR, BL, BR
"""

ZONE = [
    {
        'id': 1,
        'corners': [[5,3],[5,4],[16,3],[16,4]]
    },
    {
        'id': 2,
        'corners': [[5,8],[5,9],[16,8],[16,9]]
    },
    {
        'id': 3,
        'corners': [[5,13],[5,14],[16,13],[16,14]]
    },
    {
        'id': 4,
        'corners': [[5,18],[5,19],[16,18],[16,19]]
    }
]

def get_ZONE(location, size):
    # print('enter get_ZONE', location, 'size', size)
    zone_id = 0
    length = len(ZONE)
    print('x', location['loc_x'], 'y', location['loc_y'])
    while length > 0:
        if (ZONE[length - 1]['corners'][0][0] - size) < location['loc_x'] < (ZONE[length - 1]['corners'][2][0] + size) and (ZONE[length - 1]['corners'][0][1] - size) < location['loc_y'] < (ZONE[length - 1]['corners'][1][1] + size):
            zone_id = ZONE[length - 1]['id']
        length = length - 1
    
    return zone_id


@api_view(['GET'])
def test(request):
    # data = json.loads(request.body)
    response = {"Success": False}
    try:

        tracker_top10 = Location.objects.all()[:100]
        serializer = LocationSerializer(tracker_top10, many=True)
        location_list = serializer.data
       
        for location in location_list:
            location['product_id'] = get_ZONE(location, 1)
            
        response["data"] = location_list
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
            .annotate(max_time=Max('time'))[:limit] 
        serializer = LocationSerializer(query, many=True)
        response["data"] = serializer.data
        response["Success"] = True

        return Response(response)
    except Exception as e:
        return Response(response)

"""
    get location by tracker id
"""
@api_view(['POST'])
def getLocationBySpan(request):
    data = json.loads(request.body)
    tracker_id = data['tracker_id']
    # tracker_id = 'c60'

    response = {"Success": False}

    try:
        query = Location.objects \
            .filter(tracker_id=tracker_id)[:120]

        serializer = LocationSerializer(query, many=True)
        
        location_list = serializer.data
        for location in location_list:
            location.product_id = get_ZONE(location)
            print(location.product_id)
        response["data"] = location_list
        response["Success"] = True

        return Response(response)
    except Exception as e:
        return Response(response)



def heart_beat(data=''):
    while True:
        time.sleep(1)
        yield f'data: {datetime.datetime.now()}, {data}\n\n'


def stream_event(time_limit):
    trackers = Location.objects \
        .values('tracker_id') \
        .annotate(max_time=Max('time'))[:limit] 
    tracker_ids = [t['tracker_id'] for t in trackers]

    query = Location.objects \
        .values('time')[:time_limit] 

    time_idx = 0
    time_len = len(query)
    while True:
        time.sleep(1)
        if time_idx == time_len:
            time_idx = 0

        time_stamp = query[time_idx]['time']
        time_locations = Location.objects.filter(time=time_stamp, tracker_id__in=tracker_ids)\
            .values('tracker_id', 'loc_x', 'loc_y', 'time', 'product_id')
        length = len(time_locations)
        for item in time_locations:
            item['product_id'] = get_ZONE(item, 1)
            print(item['product_id'])

        time_locations_data = LocationSerializer(time_locations, many=True).data
        
        time_idx += 1
        # print(f'data: {json.dumps(time_locations_data)}\n\n')
        yield f'data: {json.dumps(time_locations_data)}\n\n'


@api_view(['GET'])
def sse_test(request):
    return StreamingHttpResponse(heart_beat(), content_type='text/event-stream')


# @api_view(['GET'])
def sse(request):
    print('sse')
    limit = int(request.GET.get('limit', 100))
    return StreamingHttpResponse(stream_event(limit), content_type='text/event-stream')