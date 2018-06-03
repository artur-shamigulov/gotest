from django.urls import path

from .views import (
    StatsSummaryByTestView, TestTableStatsAjaxView,
    ResultsDetailByTestView, StatsSumaryByUsersView,
    UserTableStatsAjaxView, ResultsDetailByUserView,
    ResulultsDetailedOwnView, UserTestDetailedView,
    TestLogDetailedView)

urlpatterns = [
    path(
        'summary-by-tests/',
        StatsSummaryByTestView.as_view(active_tab='summary_by_tests'),
        name="summary_by_tests"),
    path(
        'summary-by-users/',
        StatsSumaryByUsersView.as_view(active_tab='summary_by_users'),
        name="summary_by_users"),
    path(
        'summary-by-tests-ajax/<int:id>/',
        TestTableStatsAjaxView.as_view(),
        name="summary_by_tests_ajax"),
    path(
        'summary-by-users-ajax/<int:id>/',
        UserTableStatsAjaxView.as_view(),
        name="summary_by_users_ajax"),
    path(
        'detailed-by-tests/<int:id>/',
        ResultsDetailByTestView.as_view(),
        name="detailed_by_tests"),
    path(
        'detailed-by-users/<int:id>/',
        ResultsDetailByUserView.as_view(),
        name="detailed_by_users"),
    path(
        'own-stats/',
        ResulultsDetailedOwnView.as_view(),
        name="own_stats"),
    path(
        'user-test-detailed/<int:id>/<int:test_id>',
        UserTestDetailedView.as_view(),
        name="user_test_detailed"),
    path(
        'test-log-detailed/<str:uuid>',
        TestLogDetailedView.as_view(),
        name="test_log_detailed"),
]
