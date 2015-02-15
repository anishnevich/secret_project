from app.models import MovieLocation, MovieLocationSearchResult
from django.db import models
from pygeocoder import Geocoder
from geopy.distance import vincenty
from geopy.distance import great_circle
import re

class datamanager(object):
    """description of class"""

    def get_coordinates(self, address_query):
       results = Geocoder.geocode(address_query)
       return results[0].coordinates

    def get_distance(self, query_coordinates, location):
        coordinates2 = (location.latitude, location.longitude)
        return great_circle(query_coordinates, coordinates2).miles

    def get_filtered_locations(self, query_location, distance = 3, title = "*", release_year = "*", production_company = "*", distributor = "*", director = "*", writer = "*", actor = "*"):
        query_coordinates = self.get_coordinates(query_location)
        all_locations = MovieLocation.objects.all()

        locations_with_distance = map(lambda l: MovieLocationSearchResult(l, self.get_distance(query_coordinates, l)), all_locations)
        filtered_locations = filter(lambda l: l.distance <= distance, locations_with_distance)
        #title = re.compile('[a-z]+')
        return filtered_locations
