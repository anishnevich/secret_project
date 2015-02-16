"""
Definition of views.
"""

from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from app.forms import SearchForm, DataInput
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from datetime import datetime
from app.models import MovieLocation
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
    search_qs = MovieLocation.objects.filter(title__startswith=request.REQUEST['search'])
    results = set()
    for r in search_qs:
        results.add(r.title)
    resp = request.REQUEST['callback'] + '(' + json.dumps(list(results)) + ');'
    return HttpResponse(resp, content_type='application/json')

    
def index(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if (form.is_valid()):
            query = form.data['query']
            m = datamanager.datamanager()
            locations = m.get_filtered_locations(query)            
            return render(
                request, 
                'app/search_bar.html', 
                {
                    'form': form,
                     #'address': query,
                    'locations': [str(location) for location in locations], 
                })
    form = SearchForm()
    return render(request, 'app/search_bar.html', {'form': form} )

    
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )


