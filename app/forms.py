"""
Definition of forms.
"""

from django import forms
from app.models import MovieLocation

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
    """Form for all search fields."""
    query              = forms.CharField(label='Query', max_length=200, required=False)
    distance           = forms.FloatField(label='Distance', max_value=200, required=False, initial=3)
    title              = forms.CharField(label='Title', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen('title')"}), required=False)
    year               = forms.IntegerField(label='Year', max_value=2020, min_value=1880, required=False, error_messages = {'min_value': "Cinematography was only invented in 1880's."})
    production_company = forms.CharField(label='Production Company', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen('production_company')"}), required=False)
    distributor        = forms.CharField(label='Distributor', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen('distributor')"}), required=False)
    director           = forms.CharField(label='Director', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen('director')"}), required=False)
    writer             = forms.CharField(label='Writer', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen('writer')"}), required=False)
    actor              = forms.CharField(label='Actor', max_length=200, widget=forms.TextInput(attrs={"onkeyup" : "searchOpen('actor')"}), required=False)

    def clean(self):
        is_address_filled = self.cleaned_data.get('query', False)
        if is_address_filled:
            # validate the activity name
            distance = self.cleaned_data.get('distance', None)
            if distance is None:
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

