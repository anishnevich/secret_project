from app.models import MovieLocation, MovieLocationSearchResult, SearchSettings
from django.db import models
from pygeocoder import Geocoder
from geopy.distance import vincenty
from geopy.distance import great_circle
import re
from operator import attrgetter

class datamanager(object):
    """description of class"""

    def get_coordinates(self, address_query):
       results = Geocoder.geocode(address_query)
       return results[0].coordinates

    def get_distance(self, query_coordinates, location):
        coordinates2 = (location.latitude, location.longitude)
        return great_circle(query_coordinates, coordinates2).miles

    def get_filtered_locations(self, search_settings):        
        all_locations = MovieLocation.objects.all()

        filtered_locations = filter(lambda l: re.match(search_settings.title, l.title), all_locations)
        filtered_locations = filter(lambda l: re.match(search_settings.release_year, str(l.release_year)), filtered_locations)
        
        if search_settings.query_location != '' or search_settings.distance != '':
            query_coordinates = self.get_coordinates(search_settings.query_location)
            locations_with_distance = map(lambda l: MovieLocationSearchResult(l, self.get_distance(query_coordinates, l)), filtered_locations)
            filtered_locations = list(filter(lambda l: l.distance <= float(search_settings.distance), locations_with_distance))
            filtered_locations.sort(key = lambda l: l.distance)
            filtered_locations = map(lambda l: l.movie_location, filtered_locations)

        return list(filtered_locations)[:10]
