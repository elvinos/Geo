import pandas as pd
from .LocationIQInterface import LocationIQInterface
import numpy as np
import logging

logger = logging.getLogger(__name__)


class DistanceComparison:

    def compare_driving_distance(self, coords_ar_1, coords_ar_2):
        """Takes two lists (in data frame form) and calculates the distance between both
            returns a dataframe (grid) of the results
            Parameters
            ----------
            Requires 2 array of arrays - and array of [long,lat] coordinates
            i.e [[long,lat],[long,lat],[long,lat]]
            Returns
            -------
            Output:
                            0       1       2
                    0  4639.2  4061.0  3301.1
                    1  7983.7  7405.5  5283.1
                    2  3649.0  3402.8  4960.4

            x = coords_ar_1
            y = coords_ar_2
        """
        LIQ = LocationIQInterface()
        df = pd.DataFrame(np.zeros((len(coords_ar_1),len(coords_ar_2))))
        for ind_1, coords_1 in enumerate(coords_ar_1):
            time = []
            for coords_2 in coords_ar_2:
                duration, distance = LIQ.get_distance_duration(coords_1, coords_2)
                time.append(duration)
            df.iloc[ind_1]=time
        return df

    def compare_lin_distance(self, df1, df2, Name1, Name2):
        """Finds the linear (as the crow flies distance between two points
        Parameters
        ----------
        Returns
        -------
        """
        # TODO: Modify compare_lin_distance to work with app
        # df = pd.DataFrame(np.zeros((df1.shape[0], df2.shape[0])))
        # for index, df1row in tqdm(df1.iterrows(), total=df1.shape[0]):
        #     dist = []
        #     coords_1 = (df1row['Latitude'], df1row['Longitude'])
        #     for index2, df2row in df2.iterrows():
        #         coords_2 = (df2row['Latitude'], df2row['Longitude'])
        #         dist.append(geopy.distance.geodesic(coords_1, coords_2).km)
        #     df.loc[index]=dist
        # df['Name1'] = Name1
        # df=df.set_index('Name1')
        # df.columns = Name2
        # return df