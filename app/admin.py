"""
MovieLocation wrappers, used to import data to db
"""

from django.contrib import admin
from app.models import MovieLocation
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

class MovieLocationResource(resources.ModelResource):
    class Meta:
        model = MovieLocation

class MovieLocationAdmin(ImportExportModelAdmin, ImportExportMixin):
    resource_class = MovieLocationResource
    from_encoding = 'utf-8'
    pass

admin.site.register(MovieLocation, MovieLocationAdmin)
