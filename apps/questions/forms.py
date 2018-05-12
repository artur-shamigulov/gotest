from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from answers.models import Answer


class QuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answers'].queryset = question.answer_set.all()

    answers = forms.ModelMultipleChoiceField(
        queryset=Answer.objects.none(),
        widget=CheckboxSelectMultiple)
