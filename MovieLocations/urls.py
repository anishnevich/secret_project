#"""
#Definition of urls for MovieLocations.
#"""

from django.conf.urls import patterns, url, include
from app.forms import BootstrapAuthenticationForm
from datetime import datetime

from app import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.address_search, name='address_search'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/dataimport/$', 'app.views.data_import'),
    url(r'^search.json/', views.autocomplete),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
)