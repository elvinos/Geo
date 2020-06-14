# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from . import serializers
from .tools.GoogleMapsTools import GoogleMapsTools
# from .tools.DistanceTools import DistanceComparison
from .tools.DistanceTools import compare_driving_distance, increment
from .tools.DriveTimeAnalysis import DriveTimeAnalysis
from .tools.utils import convert_json_table

# from django.shortcuts import render, HttpResponse
# from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from rest_pandas import PandasSimpleView, PandasViewSet
from rest_pandas.renderers import PandasCSVRenderer, PandasBaseRenderer, PandasTextRenderer, PandasJSONRenderer, \
    PandasExcelRenderer, PandasOldExcelRenderer, PandasPNGRenderer, PandasSVGRenderer
import pandas as pd
import json

import logging

from celery.result import AsyncResult

logger = logging.getLogger(__name__)


class DriveTimeViewSet(viewsets.ViewSet):
    serializer_class = serializers.DriveTimeSerializer

    def get_renderers(self):
        if self.action == 'data':
            return [PandasCSVRenderer(), PandasCSVRenderer(), PandasBaseRenderer(), PandasTextRenderer(),
                    PandasJSONRenderer(),
                    PandasExcelRenderer(), PandasOldExcelRenderer(), PandasPNGRenderer(), PandasSVGRenderer()]
        else:
            return super().get_renderers()

    @action(detail=False)
    def data(self, *args, **kwargs):
        data = pd.read_pickle("./apps/drivetime/test_dm.pkl")
        dta = DriveTimeAnalysis(data)
        serializer_class = serializers.PanSerializer
        return Response(serializer_class(dta.create_cum_intervals(), many=True).data)

    def list(self, request):
        serializer = serializers.DriveTimeSerializer()
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def get_drivetime(self, request):
        coords_ar_1 = [['-71.3634724', '42.6159775'], ['-72.5737841411505', '42.1723059'],
                       ['-70.9682506139195', '42.55432235']]
        coords_ar_2 = [['-70.9685309348312', '42.09617755'], ['-71.0301638701927', '42.1213016'],
                       ['-71.4653062612533', '42.1162302']]
        # dc =
        response = self.run_function(request, compare_driving_distance, coords_ar_1, coords_ar_2)
        print('This is the response: %s', response)
        # logger.info(df)
        # response = df.to_json(orient='records')
        return Response(response)

    @action(detail=False)
    def get_all_data(self, *args, **kwargs):
        data = pd.read_pickle("./apps/drivetime/test_dm.pkl")
        dta = DriveTimeAnalysis(data)
        results = dta.run_full_analysis(1000)
        return Response(json.loads(results))

    @action(methods=['post'], detail=False)
    def dt_post(self, request):
        print(request.data)
        ad1, ad2 = convert_json_table(request.data)
        response = self.run_function(request, compare_driving_distance, ad1, ad2)
        return Response(response)

    def run_function(self, request, function, *args):
        if 'job' in request.GET:
            job_id = request.GET['job']
            print(job_id)
            job = AsyncResult(job_id)
            data = job.result
            context = {
                'check_status': 1,
                'data': "",
                'state': 'STARTING...',
                'task_id': job_id
            }
            return data
        else:
            job = function.apply_async(args=[*args], time_limit=600, soft_time_limit=300)
            print("Celery job ID:  {}.".format(job))
            return job.id

    @action(detail=False)
    def start_test(self, request):
        if 'job' in request.GET:
            job_id = request.GET['job']
            print(job_id)
            job = AsyncResult(job_id)
            data = job.result
            context = {
                'check_status': 1,
                'data': "",
                'state': 'STARTING...',
                'task_id': job_id
            }
            return HttpResponse(data)
        else:
            job = increment.apply_async(args=[10], time_limit=600, soft_time_limit=300)
            print("Celery job ID:  {}.".format(job))
            return Response(job.id)

    @action(detail=False)
    def update_status(self, request):
        print("Update on: {}.".format(request.GET))
        if 'task_id' in request.GET.keys():
            task_id = request.GET['task_id']
            task = AsyncResult(task_id)
            result = task.result
            status = task.status
            print(result)

        else:
            status = 'UNDEFINED!'
            result = 'UNDEFINED!'
        if status == 'SUCCESS':
            stats = {
                'status': status,
                'state': 'FINISHED',
                'iter': -1
            }
            update_res = {**result, **stats}
            print(update_res)
            return Response(update_res)
        else:
            try:
                json_data = {
                    'status': status,
                    'state': result['status'],
                    'iter': result['iteration'],
                    'total': result['total']
                }
            except TypeError:
                json_data = {
                    'status': status,
                    'state': 'FINISHED',
                    'iter': -1
                }
            return JsonResponse(json_data)


class DriveTimeAnalysisView(PandasSimpleView):

    def get_data(self, request, *args, **kwargs):
        data = pd.read_pickle("./apps/drivetime/test_dm.pkl")
        dta = DriveTimeAnalysis(data)
        return dta.create_cum_intervals()


class DTAMethodsView(viewsets.ViewSet):
    def get_renderers(self):
        if self.action == 'data':
            return [PandasCSVRenderer(), PandasCSVRenderer(), PandasBaseRenderer(), PandasTextRenderer(),
                    PandasJSONRenderer(),
                    PandasExcelRenderer(), PandasOldExcelRenderer(), PandasPNGRenderer(), PandasSVGRenderer()]
        else:
            return super().get_renderers()

    @action(detail=False)
    def data(self, *args, **kwargs):
        data = pd.read_pickle("./apps/drivetime/test_dm.pkl")
        dta = DriveTimeAnalysis(data)
        serializer_class = serializers.PanSerializer
        return Response(serializer_class(dta.create_cum_intervals(), many=True).data)
