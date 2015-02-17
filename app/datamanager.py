from app.models import MovieLocation, MovieLocationSearchResult, SearchSettings
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

    def get_filtered_locations(self, search_settings):
        query_coordinates = self.get_coordinates(search_settings.query_location)
        all_locations = MovieLocation.objects.all()

        all_locations = filter(lambda l: re.match(search_settings.title, l.title), all_locations)
        all_locations = filter(lambda l: re.match(search_settings.release_year, str(l.release_year)), all_locations)

        locations_with_distance = map(lambda l: MovieLocationSearchResult(l, self.get_distance(query_coordinates, l)), all_locations)
        filtered_locations = filter(lambda l: l.distance <= float(search_settings.distance), locations_with_distance)
        #title = re.compile('[a-z]+')

        return filtered_locations
