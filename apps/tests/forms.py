from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminSplitDateTime

from .models import Test, AppointedTest, AvailableTest
from groups.models import UserGroup

from utils.widgets import CustomAutocompleteSelectMultiple, ReactiveFilteredSelectMultiple


class TestAdminForm(forms.ModelForm):

    file_field = forms.FileField(label='Фаил теста:')

    class Meta:
        model = Test
        fields = ('__all__')


class ApointedAvailableTestFrom(forms.ModelForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=UserGroup.objects.all(),
        label='Группа', required=False,
        widget=ReactiveFilteredSelectMultiple(verbose_name="Группы", is_stacked=False))


class ApointedTestFrom(ApointedAvailableTestFrom):

    tests = forms.ModelMultipleChoiceField(
        queryset=Test.objects.all(),
        label='Тест', required=False,
        widget=CustomAutocompleteSelectMultiple(Test, admin.site))

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label='Пользователи', required=False,
        widget=CustomAutocompleteSelectMultiple(User, admin.site))

    def __init__(self, *args, **kwargs):
        users = kwargs['instance'].users.all()
        users.values_list('id').annotate()
        super(ApointedTestFrom, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        if data['datetime_start'] >= data['datetime_end']:
            raise forms.ValidationError(
                {'datetime_start': (
                    'Время начала не может '
                    'быть больше времени окончания'
                )}
            )

        group = data.get('groups')

        if group:
            users_id = list(group.values_list('users', flat=True))
            users = data.get('users')
            if users:
                users_id += list(users.values_list('id', flat=True))

            data['users'] = User.objects.filter(id__in=users_id)

        return data

    class Meta:
        model = AppointedTest
        fields = (
            'title', 'groups', 'users',
            'tests', 'duration', 'datetime_start',
            'datetime_end')
        widgets = {
            'datetime_start': AdminSplitDateTime,
            'datetime_end': AdminSplitDateTime
        }
