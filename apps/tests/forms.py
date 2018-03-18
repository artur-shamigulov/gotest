from django import forms

from .models import Test


class TestAdminForm(forms.ModelForm):

    file_field = forms.FileField(label='Фаил теста:')

    class Meta:
        model = Test
        fields = ('__all__')
