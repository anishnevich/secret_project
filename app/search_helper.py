from app.models import MovieLocation, MovieLocationSearchResult, SearchSettings
from django.db import models
from pygeocoder import Geocoder
from geopy.distance import vincenty
from geopy.distance import great_circle
import re
import operator
from functools import reduce
from operator import attrgetter
from django.db.models import Q

class search_helper(object):
    """get movies locations by address and other fields"""
    DEFAULT_LOCATIONS_NUMBER = 15

    def get_coordinates(self, address_query):
       """get coordinates by address"""
       results = Geocoder.geocode(address_query)
       return results[0].coordinates

    def get_distance(self, query_coordinates, location):
        """get distance between two locations"""
        location_coordinates = (location.latitude, location.longitude)
        return great_circle(query_coordinates, location_coordinates).miles

    def filter_by_actor(self, search_query):
        """create search args for actor field"""
        search_list = [Q(actor_1__startswith=search_query), Q(actor_2__startswith=search_query), Q(actor_3__startswith=search_query)]
        return MovieLocation.objects.filter(reduce(operator.or_, search_list))
    
    def filter_for_autocomplete(self, request):
        """search movies location by any field except address"""  
        field = request.REQUEST['field'] 
        results = set()
        if field == 'actor':
            search_qs = self.filter_by_actor(request.REQUEST['search'])
            for r in search_qs:            
                results.add(getattr(r, field + "_1"))
                results.add(getattr(r, field + "_2"))
                results.add(getattr(r, field + "_3"))
        else:
            kwargs = {            
                '{0}__{1}'.format(field, 'startswith'): request.REQUEST['search'],        
            }  
            search_qs = MovieLocation.objects.filter(**kwargs)                
            for r in search_qs:            
                results.add(getattr(r, field))
        return results;

    def get_filtered_locations(self, search_settings):
        """search movies locationby any field"""    
        all_locations = MovieLocation.objects.all()

        filtered_locations = MovieLocation.objects.filter(**search_settings.search_args)

        if search_settings.actor != '':
            filtered_locations = self.filter_by_actor(search_settings.actor)

        if search_settings.query_location != '' and search_settings.distance != '':
            query_coordinates = self.get_coordinates(search_settings.query_location)
            locations_with_distance = map(lambda l: MovieLocationSearchResult(l, self.get_distance(query_coordinates, l)), filtered_locations)
            filtered_locations = list(filter(lambda l: l.distance <= float(search_settings.distance), locations_with_distance))
            filtered_locations.sort(key = lambda l: l.distance)
            filtered_locations = map(lambda l: l.movie_location, filtered_locations)

        return list(filtered_locations)[:self.DEFAULT_LOCATIONS_NUMBER]