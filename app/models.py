"""
Definition of models.
"""

# Models are created, Master.
from django.db import models

class MovieLocation(models.Model):
    title               = models.CharField(max_length = 200, blank=False)
    release_year        = models.IntegerField(blank=False)
    locations           = models.CharField(max_length = 200, blank=False)
    fun_facts           = models.CharField(max_length = 2000, blank=True)
    production_company  = models.CharField(max_length = 200, blank=True)
    distributor         = models.CharField(max_length = 200, blank=True)
    director            = models.CharField(max_length = 200, blank=True)
    writer              = models.CharField(max_length = 200, blank=True)
    actor_1             = models.CharField(max_length = 200, blank=True)
    actor_2             = models.CharField(max_length = 200, blank=True)
    actor_3             = models.CharField(max_length = 200, blank=True)
    latitude            = models.CharField(max_length = 200, blank=False)
    longitude           = models.CharField(max_length = 200, blank=False)

    def __str__(self):
        return "Id: {2} Title: {0} Year: {1} ".format(self.title, self.release_year, self.id)


class MovieLocationSearchResult:
    def __init__(self, movie_location, distance):
        self.movie_location = movie_location
        self.distance = distance
    
    def __str__(self):
        return "MovieLocation: {0} . Distance: {1}".format(self.movie_location, self.distance)

class SearchSettings:
    DEFAULT_SEARCH_QUERY = ".*"

    def __init__(self, query_location = '', distance = '', title = '', release_year = '', production_company = '', distributor = '', director = '', writer = '', actor = ''):
        self.query_location = query_location
        self.distance = distance
        self.search_args = {            
            '{0}__{1}'.format('title', 'regex'): "^" + title if title != '' else SearchSettings.DEFAULT_SEARCH_QUERY, 
            '{0}__{1}'.format('release_year', 'regex'):  release_year if release_year != '' else SearchSettings.DEFAULT_SEARCH_QUERY, 
            '{0}__{1}'.format('production_company', 'regex'): production_company if production_company != '' else SearchSettings.DEFAULT_SEARCH_QUERY,
            '{0}__{1}'.format('distributor', 'regex'): distributor if distributor != '' else SearchSettings.DEFAULT_SEARCH_QUERY,
            '{0}__{1}'.format('director', 'regex'): director if director != '' else SearchSettings.DEFAULT_SEARCH_QUERY,
            '{0}__{1}'.format('writer', 'regex'):  writer if writer != '' else SearchSettings.DEFAULT_SEARCH_QUERY
        }

    @classmethod
    def fromform(cls, form):
        query = form.data['query']
        distance = form.data['distance']
        title = form.data['title']
        release_year = form.data['year']
        production_company = form.data['production_company']
        distributor = form.data['distributor']
        director = form.data['director']
        writer = form.data['writer']
        return cls(query, distance, title, release_year, production_company, distributor, director, writer)