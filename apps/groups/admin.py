from django.contrib import admin

from .models import UserGroup


class UserGroupAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserGroup, UserGroupAdmin)
