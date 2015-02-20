"""
Definition of views.
"""

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from app.forms import SearchForm
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from datetime import datetime
from app.models import SearchSettings
from app import search_helper
import json

def autocomplete(request):
    field = request.REQUEST['field']
    kwargs = {    
        '{0}__{1}'.format(field, 'startswith'): request.REQUEST['search'],    
    }

    searcher = search_helper.search_helper()
    search_qs = searcher.filter_by_not_address_filed(kwargs)
    results = set()
    for r in search_qs:
        results.add(getattr(r, field))
    resp = json.dumps(list(results))
    return HttpResponse(resp, content_type='application/json')
    
def address_search(request):
    assert isinstance(request, HttpRequest)
    form = SearchForm()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if (form.is_valid()):
            try:
                search_settings = SearchSettings.fromform(form)
            except:
                return HttpResponse('Bad search form', status=400)
            searcher = search_helper.search_helper()
            locations = searcher.get_filtered_locations(search_settings)   
            if not locations:
                form.errors['__all__'] = form.error_class(["No locations found"])
            return render(
                request, 
                'app/search_bar.html', 
                {
                    'form': form,
                    'locations': locations,
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


