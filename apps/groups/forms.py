from django import forms

from .models import UserGroup


class UserGroupAdminForm(forms.ModelForm):

    file_field = forms.FileField(
        label='Список пользователей', required=False)

    class Meta:
        model = UserGroup
        fields = ('__all__')
