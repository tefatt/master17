from django.conf import settings
import googlemaps
import rrdtool

class InputDataService:

    def __init__(self):
        pass

    # @staticmethod
    # def calculate_group_demand(measurements):
    #     """Formula for calculating the value for each group location of containers"""
    #     return value

    @staticmethod
    def calculate_distance(location1, location2):
        gmaps = googlemaps.Client(key=settings.GOOGLE_KEY)
        response = gmaps.distance_matrix(location1, location2)
        for property in response.get("rows"):
            # gets distance between two provided locations in meters
            distance = property.get("elements")[0].get("distance").get("value")
            return distance
        return None
