from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminSplitDateTime, FilteredSelectMultiple

from .models import Test, AppointedTest, AvailableTest
from groups.models import UserGroup

from utils.widgets import CustomAutocompleteSelectMultiple, ReactiveFilteredSelectMultiple


class TestAdminForm(forms.ModelForm):

    file_field = forms.FileField(label='Фаил теста:', required=False)

    class Meta:
        model = Test
        fields = ('__all__')


class ApointedAvailableTestFrom(forms.ModelForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=UserGroup.objects.all(),
        label='Группа', required=False,
        widget=FilteredSelectMultiple(verbose_name="Группы", is_stacked=False))

    tests = forms.ModelMultipleChoiceField(
        queryset=Test.objects.all(),
        label='Тест', required=False,
        widget=CustomAutocompleteSelectMultiple(Test, admin.site))

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label='Пользователи', required=False,
        widget=CustomAutocompleteSelectMultiple(User, admin.site))

    def clean(self):
        data = self.cleaned_data

        group = data.get('groups')

        if group:
            users_id = list(group.values_list('users', flat=True))
            users = data.get('users')
            if users:
                users_id += list(users.values_list('id', flat=True))

            data['users'] = User.objects.filter(id__in=users_id)

        return data


class ApointedTestFrom(ApointedAvailableTestFrom):

    def clean(self):
        data = super().clean()
        if data['datetime_start'] >= data['datetime_end']:
            raise forms.ValidationError(
                {'datetime_start': (
                    'Время начала не может '
                    'быть больше времени окончания'
                )}
            )

        return data

    class Meta:
        model = AppointedTest
        fields = (
            'title', 'groups', 'users',
            'tests', 'duration', 'test_size',
            'datetime_start',
            'datetime_end')
        widgets = {
            'datetime_start': AdminSplitDateTime,
            'datetime_end': AdminSplitDateTime
        }


class AvailableTestFrom(ApointedAvailableTestFrom):

    class Meta:
        model = AppointedTest
        fields = (
            'title', 'groups', 'users',
            'tests', 'test_size',)
