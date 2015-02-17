"""
Definition of forms.
"""

from django import forms
from app.models import MovieLocation

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
    query = forms.CharField(label='Query', max_length=200, required=False)
    distance = forms.IntegerField(label='Distance', max_value=200, required=False)
    title = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen()"}), required=False)
    year = forms.IntegerField(label='Year', max_value=2020, min_value=1880, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen()"}), required=False, 
                              error_messages = {'min_value': "Cinematography was only invented in 1880's."})
    
    def clean(self):
        is_address_filled = self.cleaned_data.get('query', False)
        if is_address_filled:
            # validate the activity name
            distance = self.cleaned_data.get('distance', None)
            if distance is None or not distance.isdigit():
                self._errors['distance'] = self.error_class([
                    'Distance is required when you search by address'])
        return self.cleaned_data

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class DataInput(forms.Form):
    file = forms.FileField()
    bla = forms.TextInput()

    def save(self):
        records = csv.reader(self.cleaned_data["file"])
        for line in records:
            l = MovieLocation()
            l.title = "foo"
            l.release_year = 2011
            l.locations = "here"
            l.save()

