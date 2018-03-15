from django.contrib import admin

from .models import Course

from .forms import CourseAdminForm


class CourseAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}
    form = CourseAdminForm


admin.site.register(Course, CourseAdmin)
