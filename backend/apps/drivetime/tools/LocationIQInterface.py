from __future__ import print_function
import time
import locationiq
from locationiq.rest import ApiException
from pprint import pprint
import environ
from ratelimit import limits, sleep_and_retry
import logging

logger = logging.getLogger(__name__)

class LocationIQInterface:
    """Interface for connecting to the LocationIQ Api
       Using the ratelimit package to prevent the threshold for the API being crossed
       At time of creation Location IQ accounts are limited to 2 requests per seconds
       Marked in the decorator
    """

    def __init__(self):
        self.env = environ.Env()
        self.configuration = locationiq.Configuration()
        self.configuration.api_key['key'] = self.env.str('VUE_APP_LIQ_TOKEN')
        self.configuration.host = "https://eu1.locationiq.com/v1"
        with locationiq.ApiClient(self.configuration) as api_client:
            # Create an instance of the API class
            self.api_instance = locationiq.DirectionsApi(api_client)
            self.api_instance = locationiq.DirectionsApi(api_client)

    @sleep_and_retry
    @limits(calls=2, period=1)
    def get_distance_duration(self, coords1=['-72.5737841411505','42.1723059'], coords2=['-70.9682506139195','42.55432235']):
        """Requires two pairs of coordinates: {longitude},{latitude}
           Outputs the fastest drive time and distance in seconds and m
        """
        coordinates = coords1[0].strip() +','+ coords1[1].strip() +';' + coords2[0].strip() +','+ coords2[1].strip()
        try:
#             coordinates = '-0.16102,51.523854;-0.15797,51.52326' # str | String of format {longitude},{latitude};{longitude},{latitude}[;{longitude},{latitude} ...] or polyline({polyline}) or polyline6({polyline6}). polyline follows Google's polyline format with precision 5
#             bearings = '10,20;40,30' # str | Limits the search to segments with given bearing in degrees towards true north in clockwise direction. List of positive integer pairs separated by semi-colon and bearings array should be equal to length of coordinate array. Input Value :- {bearing};{bearing}[;{bearing} ...] Bearing follows the following format : bearing {value},{range} integer 0 .. 360,integer 0 .. 180 (optional)
#             radiuses = '500;200' # str | Limits the search to given radius in meters Radiuses array length should be same as coordinates array, eaach value separated by semi-colon. Input Value - {radius};{radius}[;{radius} ...] Radius has following format :- double >= 0 or unlimited (default) (optional)
#             generate_hints = 'false' # str | Adds a Hint to the response which can be used in subsequent requests, see hints parameter. Input Value - true (default), false Format - Base64 String (optional)
#             approaches = 'curb;curb' # str | Keep waypoints on curb side. Input Value - {approach};{approach}[;{approach} ...] Format - curb or unrestricted (default) (optional)
#             exclude = 'toll' # str | Additive list of classes to avoid, order does not matter. input Value - {class}[,{class}] Format - A class name determined by the profile or none. (optional)
#             alternatives = 'true' # float | Search for alternative routes. Passing a number alternatives=n searches for up to n alternative routes. [ true, false (default), or Number ] (optional)
#             steps = 'true' # str | Returned route steps for each route leg [ true, false (default) ] (optional)
#             annotations = 'false' # str | Returns additional metadata for each coordinate along the route geometry.  [ true, false (default), nodes, distance, duration, datasources, weight, speed ] (optional) (default to '"false"')
#             geometries = 'polyline' # str | Returned route geometry format (influences overview and per step) [ polyline (default), polyline6, geojson ] (optional) (default to '"polyline"')
#             overview = 'simplified' # str | Add overview geometry either full, simplified according to highest zoom level it could be display on, or not at all. [ simplified (default), full, false ] (optional) (default to '"simplified"')
#             continue_straight = 'default' # str | Forces the route to keep going straight at waypoints constraining uturns there even if it would be faster. Default value depends on the profile [ default (default), true, false ] (optional) (default to '"default"')

            api_response = self.api_instance.directions(coordinates, annotations='false',overview = 'simplified')
            distance = api_response.routes[0].distance
            duration = api_response.routes[0].duration
            logger.info('Driving Time: %s' % duration)
            logger.info('Driving Distance: %s' % distance)
            return(duration, distance)
        except ApiException as e:
            logger.error("Exception when calling DirectionsApi->directions: %s\n" % e)
            return(None,None)