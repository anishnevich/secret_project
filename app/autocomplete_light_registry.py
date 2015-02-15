import autocomplete_light
from app.models import MovieLocation

autocomplete_light.register(MovieLocation,
    # just like in modeladmin.search_fields
    search_fields=['^title', 'release_year'],
    attrs={
        # this will set the input placeholder attribute:
        'placeholder': 'Enter location',
        # this will set the yourlabs.autocomplete.minimumcharacters
        # options, the naming conversion is handled by jquery
        'data-autocomplete-minimum-characters': 1,
    },
    # this will set the data-widget-maximum-values attribute on the
    # widget container element, and will be set to
    # yourlabs.widget.maximumvalues (jquery handles the naming
    # conversion).
    widget_attrs={
        'data-widget-maximum-values': 4,
        # enable modern-style widget !
        'class': 'modern-style',
    },
)