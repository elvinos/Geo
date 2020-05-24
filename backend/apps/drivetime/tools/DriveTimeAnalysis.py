from .DistanceTools import DistanceComparison

import pandas as pd

import numpy as np

import json

import logging

logger = logging.getLogger(__name__)


class DriveTimeAnalysis:
    """ Takes a drivetime matrix and converts to useful output
    """

    def __init__(self, data_matrix):
        self.data = data_matrix
        self.mean = pd.DataFrame
        self.mean_tot = None
        self.min_loc = pd.DataFrame
        self.min_loc_tot = pd.DataFrame
        self.intervals = None
        self.cum_intervals = None

    def calc_average_dt(self):
        """calculates the total average drivetime between both location sets

        Returns
        -------
        float of average drivetime
        """
        self.mean = self.data.mean(axis=1, skipna=True, numeric_only=True)
        self.mean_tot = self.mean.mean()
        return self.mean_tot

    def find_location_min(self):
        """finds the minimum drivetime for each location

        Returns
        -------
        Dataframe with each list a comp and the minimum drivetime of to list b and name of lowest listb
        """
        self.min_loc = self.data.min(axis=1, skipna=True, numeric_only=True)
        return self.min_loc

    def calc_average_closest_dt(self):
        """ Finds each locations closet comp location then calculates the average of these minimums
        Returns
        -------
        float of average
        """
        if self.min_loc is pd.DataFrame:
            self.min_loc = self.find_location_min()

        self.min_loc_tot = self.min_loc.mean()
        return self.min_loc_tot

    def create_intervals(self, intervals=5):
        """Creates intervals and counts the number of locations in each interval

        Parameters
        ----------
        intervals : int
            the number of intervals in mins, i.e. 5 = 5,10,15
        Returns
        -------
        Dataframe with intervals and count of each value
        """
        if self.min_loc is pd.DataFrame:
            self.min_loc = self.find_location_min()

        max_val = int(np.ceil(self.min_loc.max()))
        ranges = list(range(0, max_val+intervals, intervals))
        self.intervals = self.min_loc.groupby(pd.cut(self.min_loc.values, ranges)).count()
        return self.intervals

    def create_cum_intervals(self, intervals=5):
        """Uses intervals to a sums up the ranges cumulatively

        Parameters
        ----------
        intervals : int
            the number of intervals in mins, i.e. 5 = 5,10,15
        Returns
        -------
        Dataframe with intervals and summed count of each value
        """
        if self.intervals is None:
            self.intervals = self.create_intervals(intervals)

        self.cum_intervals = self.intervals.cumsum()
        return self.cum_intervals

    def run_full_analysis(self, intervals=5):
        self.calc_average_dt()
        self.calc_average_closest_dt()
        self.create_cum_intervals(intervals)
        self.data= self.data.to_json()
        self.mean = self.mean.to_json()
        self.min_loc = self.min_loc.to_json()
        self.intervals = self.intervals.to_json()
        self.cum_intervals = self.cum_intervals.to_json()
        return json.dumps(self.__dict__)

