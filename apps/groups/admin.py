import csv
from io import StringIO

from django.contrib import admin
from django.contrib.auth.models import User

from .models import UserGroup
from .forms import UserGroupAdminForm


class UserGroupAdmin(admin.ModelAdmin):
    form = UserGroupAdminForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        created_user_list = []
        if form.cleaned_data.get('file_field'):
            string_io = StringIO(
                form.cleaned_data.get('file_field').read().decode('utf-8'))
            user_list = csv.reader(string_io, delimiter=',', quotechar='|')

            for row in user_list:
                created_user_list.append(
                    User.objects.get_or_create(
                        username=row[0], email=row[0], password=row[1])[0])

        self.instance = obj
        self.created_user_list = created_user_list

    def save_related(self, *args, **kwargs):
        super().save_related(*args, **kwargs)
        self.instance.users.add(*self.created_user_list)


admin.site.register(UserGroup, UserGroupAdmin)
