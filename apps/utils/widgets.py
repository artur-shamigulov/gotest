from django import forms
from django.urls import reverse
from django.conf import settings
from django.contrib.admin.widgets import (
    AutocompleteSelect, AutocompleteSelectMultiple,
    FilteredSelectMultiple
)


class CustomAutocompleteSelectMultiple(AutocompleteSelectMultiple):

    def get_url(self):
        model = self.rel
        return reverse(self.url_name % (self.admin_site.name, model._meta.app_label, model._meta.model_name))


class ReactiveFilteredSelectMultiple(FilteredSelectMultiple):
    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'

        js = [
            'vendor/jquery/jquery%s.js' % extra,
            'jquery.init.js',
            'core.js',
            'SelectBox.js',
            'SelectFilter2.js',
        ]

        extra_js = ['utils/js/filtered_select_multiple.js']

        return forms.Media(js=["admin/js/%s" % path for path in js] + extra_js)
