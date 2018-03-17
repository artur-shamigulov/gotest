from django.contrib import admin

from .models import Test
from questions.models import Question


class QuestionInline(admin.StackedInline):
    extra = 0
    model = Question

    readonly_fields = ('text',)


class TestAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}

    inlines = [
        QuestionInline,
    ]


admin.site.register(Test, TestAdmin)
