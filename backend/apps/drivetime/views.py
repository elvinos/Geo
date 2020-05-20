from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from . import serializers
from .tools.GoogleMapsTools import GoogleMapsTools
from .tools.DistanceTools import DistanceComparison
import pandas as pd
import logging
logger = logging.getLogger(__name__)


class DriveTimeViewSet(viewsets.ViewSet):

    serializer_class = serializers.DriveTimeSerializer

    def list(self, request):
        serializer = serializers.DriveTimeSerializer()
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def get(self,request):
        ad1 = request.GET['ad1']
        ad2 = "144B Union Street, London, SE10LH"
#         ad2 = request.GET['ad2']
        response = GoogleMapsTools().driving_distance(ad1,ad2)
#         response = GoogleMapsTools().driving_distance("777 Brockton Avenue, Abington MA 2351","30 Memorial Drive, Avon MA 2322")
        result ="This is a test"
        return(JsonResponse(response, safe=False))

    @action(methods=['GET'], detail=False)
    def get_drivetime(self,request):
        coords_ar_2 = [['-70.9685309348312','42.09617755'],
                      ['-71.0301638701927','42.1213016'],
                      ['-71.4653062612533','42.1162302']]

        coords_ar_1 = [['-71.3634724','42.6159775'],
                       ['-72.5737841411505','42.1723059'],
                       ['-70.9682506139195','42.55432235']]

        df = DistanceComparison().compare_driving_distance(coords_ar_1,coords_ar_2)
        logger.info(df)
        response = df.to_json(orient='records')
        return(JsonResponse(response, safe=False))

    def sendsometext(self):
        return("This is some text")
