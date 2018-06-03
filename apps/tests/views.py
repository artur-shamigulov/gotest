from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, RedirectView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.mixins import SidebarBaseMixin, NavBaseMixin

from .models import Test, AppointedTest, AvailableTest, TestLog
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
        return reverse_lazy(
            'tests:test',
            kwargs={'uuid': test_log.test_uid, 'page': 1})


class StartAppointedTestView(
        LoginRequiredMixin,
        RedirectView):

    def get_redirect_url(self, slug, **kwargs):
        test = get_object_or_404(Test, slug=slug)

        appointed_test = get_list_or_404(
            AppointedTest, users=self.request.user, tests=test
        )[0]

        test_log = test.start_test(
            self.request.user,
            duration=appointed_test.duration, length=appointed_test.test_size)
        test_log.appointed_test = appointed_test
        test_log.save()
        return reverse_lazy(
            'tests:test',
            kwargs={'uuid': test_log.test_uid, 'page': 1})


class TestView(
        LoginRequiredMixin,
        NavBaseMixin,
        SidebarBaseMixin,
        FormView):

    form_class = QuestionForm
    template_name = 'tests/test.html'

    def no_question_response(self):
        raise Http404

    def dispatch(self, request, uuid, page, *args, **kwargs):
        self.test = Test.get_test(uuid)
        if not self.test:
            raise Http404

        self.question = self.test.set_current_question(page - 1)
        if isinstance(self.question, (NoQuestionBase,)):
            self.no_question_response()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['test'] = self.test
        ctx['question'] = self.question
        return ctx

    def get_initial(self):
        answers = self.test.get_answer()
        return {
            'answers': answers and answers.values_list('id', flat=True) or []
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question'] = self.question
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        self.test.set_answer(
            data['answers']
        )

        if data.get('complete_test'):
            Test.end_test(self.test.test_uid)
            return HttpResponseRedirect(
                reverse_lazy(
                    'tests:complete_test',
                    kwargs={
                        'uuid': self.test.test_uid}
                )
            )
        return HttpResponseRedirect(
            reverse_lazy(
                'tests:test',
                kwargs={
                    'uuid': self.test.test_uid,
                    'page': data['next'] + 1})
        )


class CompleteTestView(TestListBaseView):

    template_name = 'tests/completed_test.html'

    def dispatch(self, request, uuid, *args, **kwargs):
        self.test = get_object_or_404(
            TestLog, test_uid=self.kwargs['uuid'])
        return super().dispatch(request, uuid, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['test'] = self.test
        ctx['estimate'] = self.test.score
        return ctx
