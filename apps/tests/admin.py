from django.contrib import admin

from .models import Test
from .forms import TestAdminForm
from .parserDoc import get_full_text
from .parser import pasre_test_format
from questions.models import Question
from answers.models import Answer


class QuestionInline(admin.StackedInline):
    extra = 0
    model = Question

    readonly_fields = ('text',)


class TestAdmin(admin.ModelAdmin):

    form = TestAdminForm

    prepopulated_fields = {"slug": ("title",)}

    inlines = [
        QuestionInline,
    ]

    def save_model(self, request, obj, form, change):
        super(TestAdmin, self).save_model(request, obj, form, change)
        obj.question_set.all().delete()
        question_list = pasre_test_format(
            get_full_text(
                form.cleaned_data['file_field'].file
            )
        )

        for question in question_list:
            instance = Question.objects.create(
                test=obj,
                text=question['text']
            )
            answers = []
            for answer in question['answers']:
                answers.append(
                    Answer(text=answer, question=instance))
            Answer.objects.bulk_create(answers)


admin.site.register(Test, TestAdmin)
