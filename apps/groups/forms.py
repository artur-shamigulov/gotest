from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User

from .models import UserGroup


class UserGroupAdminForm(forms.ModelForm):

    file_field = forms.FileField(
        label='Список пользователей', required=False)
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label='Список пользователей',
        widget=FilteredSelectMultiple('Пользователи', is_stacked=False),
        required=False)

    class Meta:
        model = UserGroup
        fields = ('__all__')
