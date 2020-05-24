# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from . import serializers
from .tools.GoogleMapsTools import GoogleMapsTools
from .tools.DistanceTools import DistanceComparison
from .tools.DriveTimeAnalysis import DriveTimeAnalysis
import drivetime.tools.utils as utils

from rest_pandas import PandasSimpleView, PandasViewSet
from rest_pandas.renderers import PandasCSVRenderer, PandasBaseRenderer, PandasTextRenderer, PandasJSONRenderer, \
    PandasExcelRenderer, PandasOldExcelRenderer, PandasPNGRenderer, PandasSVGRenderer
import pandas as pd
import json

import logging

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

    # @action(methods=['GET'], detail=False)
    # def get(self, request):
    #     # ad1 = request.GET['ad1']
    #     ad2 = "144B Union Street, London, SE10LH"
    #     #         ad2 = request.GET['ad2']
    #     response = GoogleMapsTools().driving_distance(ad1, ad2)
    #     #         response = GoogleMapsTools().driving_distance("777 Brockton Avenue, Abington MA 2351","30 Memorial Drive, Avon MA 2322")
    #     return (JsonResponse(response, safe=False))

    @action(methods=['GET'], detail=False)
    def get_drivetime(self, request):
        coords_ar_2 = [['-70.9685309348312', '42.09617755'],
                       ['-71.0301638701927', '42.1213016'],
                       ['-71.4653062612533', '42.1162302']]

        coords_ar_1 = [['-71.3634724', '42.6159775'],
                       ['-72.5737841411505', '42.1723059'],
                       ['-70.9682506139195', '42.55432235']]

        df = DistanceComparison().compare_driving_distance(coords_ar_1, coords_ar_2)
        logger.info(df)
        response = df.to_json(orient='records')
        return (JsonResponse(response, safe=False))

    @action(detail=False)
    def get_all_data(self, *args, **kwargs):
        data = pd.read_pickle("./apps/drivetime/test_dm.pkl")
        dta = DriveTimeAnalysis(data)
        results = dta.run_full_analysis(1000)
        return Response(json.loads(results))

    @action(methods=['post'], detail=False)
    def dt_post(self, request):
        ad1, ad2 = utils.convert_json_table(request.data)
        print(request.data)
        print(ad1)
        print(ad2)
        df = DistanceComparison().compare_driving_distance(ad1, ad2)
        dta = DriveTimeAnalysis(df)
        results = dta.run_full_analysis(1000)
        # print(results)
        return Response(json.loads(results))

    @action(detail=False)
    def get_all_data_test(self, *args, **kwargs):
        data = pd.read_pickle("./apps/drivetime/test_dm.pkl")
        dta = DriveTimeAnalysis(data)
        results = dta.run_full_analysis(1000)
        return Response(json.loads(results))


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
