"""
Definition of forms.
"""

from django import forms
from app.models import MovieLocation

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
    query = forms.CharField(label='Query', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen()"}))

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

