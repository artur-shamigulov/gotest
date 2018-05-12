from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import TemplateView, RedirectView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.mixins import SidebarBaseMixin, NavBaseMixin

from .models import Test, AppointedTest, AvailableTest
from questions.forms import QuestionForm

from .utils import NoQuestionBase


class TestListBaseView(
        LoginRequiredMixin,
        NavBaseMixin,
        SidebarBaseMixin,
        TemplateView):

    template_name = 'tests/test_list.html'
    _title = ''

    def title(self):
        return self._title

    @staticmethod
    def get_test(user):
        return []

    def tests(self):
        return self.get_test(
            self.request.user)


class ApointedTestListView(TestListBaseView):

    template_name = 'tests/appointed_test_list.html'
    _title = 'Назначенные тесты'

    @staticmethod
    def get_test(user):
        return AppointedTest.objects.future(
            users=user).prefetch_related('tests')


class AvailableTestListView(TestListBaseView):

    template_name = 'tests/available_test_list.html'
    _title = 'Доступные тесты'

    @staticmethod
    def get_test(user):
        return Test.objects.filter(availabletest__users=user)


class StartAvailableTestView(
        LoginRequiredMixin,
        RedirectView):

    def get_redirect_url(self, slug, **kwargs):
        test = get_object_or_404(Test, slug=slug)

        available_test = get_list_or_404(
            AvailableTest, users=self.request.user, tests=test
        )[0]

        test_log = test.start_test(
            self.request.user,
            duration=available_test.duration, length=available_test.test_size)
        test_log.available_test = available_test
        test_log.save()
        return reverse_lazy('tests:test', kwargs={'uuid': test_log.test_uid})


class TestView(
        LoginRequiredMixin,
        NavBaseMixin,
        SidebarBaseMixin,
        FormView):

    from_class = QuestionForm
    template_name = 'tests/test.html'

    def dispatch(self, request, uuid, *args, **kwargs):
        self.test = Test.get_test(uuid)
        if not self.test:
            raise Http404

        self.question = self.test.current_question()
        if isinstance(self.question, (NoQuestionBase,)):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['test'] = self.test
        return ctx

    def get_form(self, from_class=None):
        return self.from_class(
            question=self.question)







