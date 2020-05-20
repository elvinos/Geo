from .DistanceTools import DistanceComparison

import pandas as pd

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


    def calc_average_dt(self):
        """calculates the total average drivetime between both location sets

        Returns
        -------
        float of average drivetime
        """
        self.mean = self.data.mean(axis=1, skipna=True,numeric_only=True)
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

    def create_cumulative_intervals(self, intervals=5):
        """Creates the cumulative intervals and counts the number of locations in each interval

        Parameters
        ----------
        intervals : int
            the number of intervals in mins, i.e. 5 = 5,10,15
        Returns
        -------
        Dataframe with intervals and count of each value
        """
        #TODO: create_cumulative_intervals

    def create_bucket_intervals(self, intervals=5):
        """Creates discrete buckets and counts minimums in each bucket

        Parameters
        ----------
        intervals : int
            the number of intervals in mins, i.e. 5 = 5,10,15
        Returns
        -------
        Dataframe with intervals and count of each value
        """
        #TODO: create_bucket_intervals