from django.forms.widgets import Textarea


class HTMLTextareaWidget(Textarea):

    template_name = 'tests/HTMLAreaWidget.html'