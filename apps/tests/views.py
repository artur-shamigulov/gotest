from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.mixins import SidebarBaseMixin, NavBaseMixin


class TestListBaseView(
        LoginRequiredMixin,
        NavBaseMixin,
        SidebarBaseMixin,
        TemplateView):

    template_name = 'tests/test_list.html'
    _title = ''

    def title(self):
        return self._title


class ApointedTestListView(TestListBaseView):

    _title = 'Назначенные тесты'


class AvailableTestListView(TestListBaseView):

    _title = 'Доступные тесты'
