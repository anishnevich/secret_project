from django.contrib import admin
from app.models import MovieLocation
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

#class MovieLocationAdmin(admin.ModelAdmin):
#    actions = [make_published]

class MovieLocationResource(resources.ModelResource):
    #title               = fields.Field(column_name='Title')
    #release_year        = fields.Field(column_name='Release Year')
    #locations           = fields.Field(column_name='Locations')
    #fun_facts           = fields.Field(column_name='Fun Facts')
    #production_company  = fields.Field(column_name='Production Company')
    #distributor         = fields.Field(column_name='Distributor')
    #director            = fields.Field(column_name='Director')
    #writer              = fields.Field(column_name='Writer')
    #actor_1             = fields.Field(column_name='Actor 1')
    #actor_2             = fields.Field(column_name='Actor 2')
    #actor_3             = fields.Field(column_name='Actor 3')

    class Meta:
        model = MovieLocation

class MovieLocationAdmin(ImportExportModelAdmin, ImportExportMixin):
    resource_class = MovieLocationResource
    from_encoding = 'utf-8'
    pass

admin.site.register(MovieLocation, MovieLocationAdmin)
