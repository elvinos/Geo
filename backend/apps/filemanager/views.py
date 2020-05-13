# from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from apps.filemanager.models import Data
from apps.filemanager.serializers import DataSerializer

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
