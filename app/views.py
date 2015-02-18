"""
Definition of views.
"""

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from app.forms import SearchForm, DataInput
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from datetime import datetime
from app.models import MovieLocation, SearchSettings
from django.contrib.admin.views.decorators import staff_member_required
from app import datamanager
import json

@staff_member_required
def data_import(request):
    if request.method == "POST":
        form = DataInput(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success = True
            context = {"form": form, "success": success}
            return render(request, "app/data_import.html", context)
    else:
        form = DataInput()        
        context = {"form": form}
        return render(request, "app/data_import.html", context) 

def autocompleteModel(request):
    field = request.REQUEST['field']
    kwargs = {    
        '{0}__{1}'.format(field, 'startswith'): request.REQUEST['search'],    
    }
    search_qs = MovieLocation.objects.filter(**kwargs)
    results = set()
    for r in search_qs:
        results.add(r.title)
    resp = json.dumps(list(results))
    return HttpResponse(resp, content_type='application/json')

    
def address_search(request):
    assert isinstance(request, HttpRequest)
    form = SearchForm()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if (form.is_valid()):
            search_settings = SearchSettings.fromform(form)
            m = datamanager.datamanager()
            locations = m.get_filtered_locations(search_settings)            
            return render(
                request, 
                'app/search_bar.html', 
                {
                    'form': form,
                     #'address': query,
                    'locations': [str(location) for location in locations], 
                })
    
    return render(request, 'app/search_bar.html', {'form': form} )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Here is a service that shows on a map where movies have been filmed in San Francisco.',
            'year':datetime.now().year,
        })
    )


