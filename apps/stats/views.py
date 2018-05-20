from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.mixins import SidebarBaseMixin, NavBaseMixin

from tests.models import (
    Test, AppointedTest, AvailableTest, TestLog)

from courses.models import Course


class StatsBaseView(
        LoginRequiredMixin,
        NavBaseMixin,
        SidebarBaseMixin):

    pass


class StatsSummaryByTestView(StatsBaseView, TemplateView):

    template_name = 'stats/by_tests_static.html'

    def get_courses(self):
        return Course.objects.all()


class BaseStatsAjaxView(LoginRequiredMixin, TemplateView):
    pass


class TableStatsAjaxView(LoginRequiredMixin, TemplateView):

    template_name = "stats/stats_table_by_test.html"

    def rows(self):
        return Test.objects.filter(course=self.kwargs['id'])
