from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import (
    Avg, Max, Case, When, IntegerField, Count, F, Q, Sum)
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from main.mixins import SidebarBaseMixin, NavBaseMixin

from tests.models import (
    Test, AppointedTest, AvailableTest, TestLog)

from courses.models import Course
from groups.models import UserGroup


class StatsBaseView(
        LoginRequiredMixin,
        NavBaseMixin,
        PermissionRequiredMixin,
        SidebarBaseMixin):

    permission_required = 'tests.can_read_stats'
    login_url = reverse_lazy('account:login')


class StatsSummaryByTestView(StatsBaseView, TemplateView):

    template_name = 'stats/by_tests_static.html'

    def get_courses(self):
        return Course.objects.all()


class StatsSumaryByUsersView(StatsBaseView, TemplateView):
    template_name = 'stats/by_users_static.html'

    def get_groups(self):
        return UserGroup.objects.all()


class BaseStatsAjaxView(LoginRequiredMixin, TemplateView):
    pass


class TestTableStatsAjaxView(LoginRequiredMixin, TemplateView):
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


class UserTableStatsAjaxView(LoginRequiredMixin, TemplateView):
    template_name = "stats/stats_table_by_user.html"

    def rows(self):
        return User.objects.filter(
            usergroup=self.kwargs['id']
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


class ResultsDetailByUserView(StatsBaseView, TemplateView):

    template_name = 'stats/detail_results_by_user.html'

    def get_user_id(self):
        return self.kwargs['id']

    def rows(self):
        return list(TestLog.objects.filter(
            user=self.get_user_id()
        ).values('test__id').annotate(
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
            'test__title', 'max_appointed', 'avg_available'
        )) + list(Test.objects.filter(
            Q(availabletest__users=self.get_user_id()) |
            Q(appointedtest__users=self.get_user_id())
        ).annotate(
            test_log_count=Sum(Case(
                When(
                    testlog__user_id=self.get_user_id(), then=1),
                default=0,
                output_field=IntegerField()
            )),
            test__title=F('title'),
        ).filter(test_log_count=0).values('test__title'))
