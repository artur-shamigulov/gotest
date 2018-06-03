from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import (
    Avg, Max, Case, When, IntegerField, Count, F, Q, Sum)
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import Http404

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

    def title(self):
        return Test.objects.get(id=self.kwargs['id'])

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
            'user__username', 'user__id', 'max_appointed', 'avg_available'
        )) + list(User.objects.filter(
            Q(availabletest__tests=self.kwargs['id']) |
            Q(appointedtest__tests=self.kwargs['id'])
        ).annotate(
            test_log_count=Count('testlog'),
            user__username=F('username'),
            user__id=F('id'),
        ).filter(test_log_count=0).values('user__username', 'user__id'))


class ResultsDetailByUserView(StatsBaseView, TemplateView):

    template_name = 'stats/detail_results_by_user.html'

    def get_user_id(self):
        return self.kwargs['id']

    def title(self):
        return User.objects.get(id=self.kwargs['id'])

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
            'test__title', 'test__id', 'max_appointed', 'avg_available'
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
            test__id=F('id'),
        ).filter(test_log_count=0).values('test__title', 'test__id'))


class ResulultsDetailedOwnView(ResultsDetailByUserView):

    template_name = 'stats/own_detailed_result.html'

    def get_permission_required(self):
        return tuple()

    def get_user_id(self):
        return self.request.user.id


class UserTestDetailedView(LoginRequiredMixin,
                           NavBaseMixin,
                           SidebarBaseMixin,
                           TemplateView):

        template_name = 'stats/user_test_detailed.html'

        def get_user_id(self):
            if self.request.user.has_perm('tests.can_read_stats'):
                return self.kwargs['id']
            return self.request.user.id

        def total_stats(self):
            return TestLog.objects.filter(
                test=self.kwargs['test_id'],
                user=self.get_user_id()
            ).aggregate(
                train_count=Sum(Case(
                    When(available_test__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField())
                ),
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
            )

        def appointed_list(self):
            return AppointedTest.objects.filter(
                tests=self.kwargs['test_id'],
                users=self.get_user_id()
            ).annotate(
                datetime_started=F('testlog__datetime_created'),
                datetime_ended=F('testlog__datetime_completed'),
                score=F('testlog__score'),
                uuid=F('testlog__test_uid'),
            ).order_by('testlog__datetime_created')

        def available_list(self):
            return AvailableTest.objects.filter(
                tests=self.kwargs['test_id'],
                users=self.get_user_id()
            ).annotate(
                datetime_started=F('testlog__datetime_created'),
                datetime_ended=F('testlog__datetime_completed'),
                score=F('testlog__score'),
                uuid=F('testlog__test_uid'),
            ).order_by('testlog__datetime_created')


class TestLogDetailedView(
        LoginRequiredMixin,
        NavBaseMixin,
        SidebarBaseMixin,
        TemplateView):

    template_name = 'stats/test_log_detailed.html'

    def get_test_log(self):
        test_log = TestLog.objects.filter(
            test_uid=self.kwargs['uuid']
        ).prefetch_related(
            'questionlog_set', 'questionlog_set__answerlog_set',
            'questionlog_set__question',
            'questionlog_set__answerlog_set__answer')
        if not self.request.user.has_perm('tests.can_read_stats'):
            test_log = test_log.filter(user_id=self.request.user.id)
        test_log = test_log.first()
        if not test_log:
            raise Http404
        return test_log
