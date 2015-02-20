"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

import django
from django.test import TestCase

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests for the application views."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            django.setup()

    def test_about(self):
        """Tests the about page."""
        response = self.client.get('/about')
        self.assertContains(response, 'SF Movies', 3, 200)      

class SearchFormTest(TestCase):
    """Tests for the search."""

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            django.setup()

    def test_search_misformed_post(self):
        """Tests search with empty POST request"""
        response = self.client.post('/', {})
        self.assertEqual(response.status_code, 400)

    def test_search_by_title(self):
        """Tests search by title."""
        response = self.client.post('/', {'query': '','distance': '','year': '', 'title': 'Need For Speed', 
        'production_company':'','distributor':'','director':'','writer':''})
        self.assertContains(response, 'Need For Speed', count=9, status_code=200)

    def test_search_by_year(self):
        """Tests search by title."""
        response = self.client.post('/', {'query': '','distance': '','year': '1973', 'title': '', 
        'production_company':'','distributor':'','director':'','writer':''})
        self.assertContains(response, 'Magnum Force', count=9, status_code=200)
        self.assertContains(response, 'American Graffiti ', count=9, status_code=200)
        
class AutoCompleteTest(TestCase):
    """Tests for autocomplete."""
        
    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            django.setup()

    def test_title_autocompletion(self):
        """Tests autocompletion for title."""
        response = self.client.post('/search.json/', {'field': 'title', 'search' : 'Need'})
        self.assertContains(response, 'Need For Speed', count=1, status_code=200)
        response = self.client.post('/search.json/', {'field': 'title', 'search' : 'Sis'})
        self.assertContains(response, 'Sister Act', count=2, status_code=200)

    def test_title_autocompletion_with_empty_result(self):
        """Tests autocompletion for title."""
        response = self.client.post('/search.json/', {'field': 'title', 'search' : 'Need1'})
        self.assertContains(response, 'Need For Speed', count=0, status_code=200)

    def test_production_company_autocompletion(self):
        """Tests autocompletion for production_company."""
        response = self.client.post('/search.json/', {'field': 'production_company', 'search' : 'Mission'})
        self.assertContains(response, 'Mission Street Producitons, LLC', count=1, status_code=200)
        
    def test_distributor_autocompletion(self):
        """Tests autocompletion for distributor."""
        response = self.client.post('/search.json/', {'field': 'distributor', 'search' : 'HBO'})
        self.assertContains(response, 'Home Box Office (HBO)', count=1, status_code=200)

    def test_director_autocompletion(self):
        """Tests autocompletion for director."""
        response = self.client.post('/search.json/', {'field': 'director', 'search' : 'Andrew'})
        self.assertContains(response, 'Andrew Haigh', count=1, status_code=200)
        self.assertContains(response, 'Andrew Lau', count=1, status_code=200)

    def test_writer_autocompletion(self):
        """Tests autocompletion for writer."""
        response = self.client.post('/search.json/', {'field': 'writer', 'search' : 'Mi'})
        self.assertContains(response, 'Michael Lannan', count=1, status_code=200)
        self.assertContains(response, 'Mitchell Kapner', count=1, status_code=200)