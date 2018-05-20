from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Max, Case, When, IntegerField, Count, F, Q
from django.contrib.auth.models import User

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
        return Test.objects.filter(
            course=self.kwargs['id']
        ).annotate(
            avg_available=Avg(
                Case(
                    When(
                        testlog__available_test__isnull=False, then='testlog__score'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            avg_appointed=Avg(
                Case(
                    When(
                        testlog__appointed_test__isnull=False, then='testlog__score'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
        )


class ResultsDetailByTestView(StatsBaseView, TemplateView):

    template_name = 'stats/detail_results_by_test.html'

    def rows(self):
        return list(TestLog.objects.filter(
            test=self.kwargs['id']
        ).values('user__username').annotate(
            avg_available=Avg(
                Case(
                    When(
                        available_test__isnull=False, then='score'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
            max_appointed=Max(
                Case(
                    When(
                        appointed_test__isnull=False, then='score'),
                    default=0,
                    output_field=IntegerField()
                )
            ),
        ).values(
            'user__username', 'max_appointed', 'avg_available'
        )) + list(User.objects.filter(
            Q(availabletest__tests=self.kwargs['id']) |
            Q(appointedtest__tests=self.kwargs['id'])
        ).annotate(
            test_log_count=Count('testlog'),
            user__username=F('username'),
        ).filter(test_log_count=0).values('user__username'))
