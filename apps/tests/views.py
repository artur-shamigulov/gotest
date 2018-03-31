from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.mixins import SidebarBaseMixin, NavBaseMixin

from .models import Test, AppointedTest


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
