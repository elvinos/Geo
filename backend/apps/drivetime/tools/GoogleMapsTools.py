import googlemaps
from datetime import datetime
import environ

class GoogleMapsTools:
    def __init__(self):
        """
        Initialise the class
        """
        self.env = environ.Env()
        self.KEY = self.env.str('VUE_APP_GMAPS_API')
        self.gmaps = googlemaps.Client(key=self.KEY)

    def __repr__(self):
        return "Class used to extract data from google maps"

    def driving_distance(self, address1, address2, minutes=True):
        now = datetime.now()
#         try:
        directions_result = self.gmaps.directions(str(address1), str(address2), mode="driving", avoid="ferries", departure_time=now)
        if len(directions_result) > 0:
            if minutes == True:
                time = str(directions_result[0]['legs'][0]['duration']['text']).split()
                if len(time) > 2:
                    return int(time[0])*60 + int(time[2])
                else:
                    return int(time[0])
            else:
                return directions_result[0]['legs'][0]['duration']['text']
        else:
            return('Unable to get: ', address1, address2)