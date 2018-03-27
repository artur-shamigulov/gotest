from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

from .models import (
    Test, AppointedTest, AvailableTest)
from .forms import TestAdminForm, ApointedTestFrom
from .parserDoc import get_full_text
from .parser import pasre_test_format
from questions.models import Question
from answers.models import Answer


class QuestionInline(admin.StackedInline):
    extra = 0
    model = Question
    exclude = ('text',)

    readonly_fields = ('question_text',)

    def question_text(self, instance):

        return format_html(
            mark_safe('<br>%s</br><a href="%s">Редактировать</a>' % (
                instance.text,
                str(reverse_lazy('admin:questions_question_change', args=(
                    instance.id,)))
            )),)

    question_text.short_description = "Вопрос"


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
                    Answer(
                        text=answer['text'],
                        is_true=answer['is_true'],
                        question=instance))
            Answer.objects.bulk_create(answers)


admin.site.register(Test, TestAdmin)


class AppointedTestAdmin(admin.ModelAdmin):

    form = ApointedTestFrom

    def get_form(self, *args, **kwargs):
        return self.form


admin.site.register(AppointedTest, AppointedTestAdmin)


class AvailableTestAdmin(admin.ModelAdmin):
    pass


admin.site.register(AvailableTest, AvailableTestAdmin)
