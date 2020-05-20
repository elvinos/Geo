from django.test import TestCase
from .tools.GoogleMapsTools import GoogleMapsTools
from .tools.LocationIQInterface import LocationIQInterface
from .tools.DistanceTools import DistanceComparison
from .tools.DriveTimeAnalysis import DriveTimeAnalysis
import pandas as pd

# Create your tests here.

class GMapsTest(TestCase):

    def setUp(self):
        self.liq = LocationIQInterface()
#         gmt = GoogleMapsTools()
#
#     def test_driving_distance(self):
#         res = GoogleMapsTools().driving_distance("4 Beagley Close, Hartley Wintney, RG278FB","144B Union Street, London, SE10LH")
#         print(res)
#     def test_locationiq(self):
#         LocationIQInterface().get_distance_duration()

#     def test_distance_tools(self):
#         coords_ar_2 = [['-70.9685309348312','42.09617755'],
#                       ['-71.0301638701927','42.1213016'],
#                       ['-71.4653062612533','42.1162302']]
#
#         coords_ar_1 = [['-71.3634724','42.6159775'],
#                        ['-72.5737841411505','42.1723059'],
#                        ['-70.9682506139195','42.55432235']]
#
#         df = DistanceComparison().compare_driving_distance(coords_ar_1,coords_ar_2)
#         print(df)
#         self.data = df
#         df.to_pickle("./apps/drivetime/test_dm.pkl")

    def test_distance_analyis(self):
        data = pd.read_pickle("./apps/drivetime/test_dm.pkl")
        dta = DriveTimeAnalysis(data)
        print(dta.find_location_min())
        print(dta.calc_average_closest_dt())
#         print(dta.calc_average_closest_dt)
#
#         print(dta.create_cumulative_intervals)
#         print(dta.create_bucket_intervals)



