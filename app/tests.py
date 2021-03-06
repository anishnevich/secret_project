"""
This is unit tests. 
All hardcoded counts calcualte based on test data.
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
    """
    Tests for the search. 
    All magic numbers are calculated as N = (number of search result) * 2 (+ 1). +1 only in search by title. 
    As titles appear twice on marker and one comes from search form, if we search by title
    """

    EMPTY_SEARCH_QUERY = {
        'query': '',
        'distance': '',
        'year': '',
        'title': '', 
        'production_company':'',
        'distributor':'',
        'director':'',
        'writer':'',
        'actor': ''
    }

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
        q = self.EMPTY_SEARCH_QUERY.copy()
        q['title'] = 'Need For Speed'
        response = self.client.post('/', q)
        self.assertContains(response, 'Need For Speed', count=9, status_code=200)

    def test_search_by_year(self):
        """Tests search by title."""
        q = self.EMPTY_SEARCH_QUERY.copy()
        q['year'] = '1973'
        response = self.client.post('/', q)
        self.assertContains(response, 'Magnum Force', count=24, status_code=200)
        self.assertContains(response, 'American Graffiti', count=2, status_code=200)

    def test_search_by_address_without_distance(self):
        """Tests search by title."""
        q = self.EMPTY_SEARCH_QUERY.copy()
        q['query'] = '60 Spear Street'
        response = self.client.post('/', q)
        self.assertContains(response, 'Distance is required when you search by address', count=1, status_code=200)

    def test_search_by_address(self):
        """Tests search by title."""
        q = self.EMPTY_SEARCH_QUERY.copy()
        q['query'] = '60 Spear Street'
        q['distance'] = 3.0
        response = self.client.post('/', q)
        self.assertContains(response, 'Nine Months', count=2, status_code=200)

    def test_search_by_actor_3(self):
        """Tests search by actor specified in actor_3 field."""
        q = self.EMPTY_SEARCH_QUERY.copy()
        q['actor'] = 'Michael Keaton'
        response = self.client.post('/', q)
        self.assertContains(response, 'My Reality', count=4, status_code=200)

    def test_search_by_actor_2(self):
        """Tests search by actor specified in actor_3 field."""
        q = self.EMPTY_SEARCH_QUERY.copy()
        q['actor'] = 'Sharon Stone'
        response = self.client.post('/', q)
        self.assertContains(response, 'Basic Instinct', count=12, status_code=200)
        self.assertContains(response, 'Sphere', count=2, status_code=200)

    def test_search_by_actor_1_and_2(self):
        """Tests search by actor specified in actor_3 field."""
        q = self.EMPTY_SEARCH_QUERY.copy()
        q['actor'] = 'Dustin Hoffman'
        response = self.client.post('/', q)
        self.assertContains(response, 'The Graduate', count=2, status_code=200)
        self.assertContains(response, 'Sphere', count=2, status_code=200)

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
        response = self.client.post('/search.json/', {'field': 'distributor', 'search' : 'NA'})
        self.assertContains(response, 'NA', count=2, status_code=200)

    def test_distributor_autocompletion_empty_result(self):
        """Tests autocompletion for distributor."""
        response = self.client.post('/search.json/', {'field': 'distributor', 'search' : 'XXX'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.content), 2) # '[]'

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
        
    def test_actor_autocompletion(self):
        """Tests autocompletion for actor. Check that we grab data from all three actors fields"""
        response = self.client.post('/search.json/', {'field': 'actor', 'search' : 'Sam'})
        self.assertContains(response, 'Samuel L. Jackson', count=1, status_code=200)
        self.assertContains(response, 'Sam Elliot', count=1, status_code=200)
        self.assertContains(response, 'Sam Shepard', count=1, status_code=200)