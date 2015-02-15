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

