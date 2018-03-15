from django.contrib import admin

from .models import Test


class TestAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Test, TestAdmin)
