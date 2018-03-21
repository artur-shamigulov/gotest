from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from questions.models import Question
from answers.models import Answer


class AnswerInline(admin.StackedInline):
    extra = 0
    model = Answer
    exclude = ('text',)

    readonly_fields = ('answer_text',)

    def answer_text(self, instance):

        return format_html(
            mark_safe('<br>%s</br><a href="%s">Редактировать</a>' % (
                instance.text,
                str(reverse_lazy('admin:answers_answer_change', args=(
                    instance.id,)))
            )),)

    answer_text.short_description = "Ответ"


class QuestionAdmin(admin.ModelAdmin):

    inlines = [
        AnswerInline,
    ]


admin.site.register(Question, QuestionAdmin)
