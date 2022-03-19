import json
import uuid

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from map.models import (Tracker, Location, Setting)
from .serializers import (LocationSerializer, TrackerSerializer)
from map import serializers

# Create your views here.
@api_view(['GET'])
def test(request):
    # data = json.loads(request.body)
    response = {"Success": False}
    try:
   
        tracker_top10 = Location.objects.all()[ :10]
        serializer = LocationSerializer(tracker_top10, many=True)
        
        response["data"]=serializer.data
        response["Success"]=True
        
        return Response(response)
    except Exception as e:
        return Response(response)