from django import forms

from .models import Course
from apps.tests.models import Test


class CourseAdminForm(forms.ModelForm):

    tests = forms.ModelMultipleChoiceField(queryset=Test.objects.all())

    def clean_title(self):
        print (self.cleaned_data)
        if len(self.cleaned_data['title']) > 10:
            raise forms.ValidationError('Поле слишком длинное')
        return self.cleaned_data['title']

    class Meta:
        model = Course
        fields = ('__all__')
