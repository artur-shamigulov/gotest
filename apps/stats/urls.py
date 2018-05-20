from django.urls import path

from .views import (
    StatsSummaryByTestView, TableStatsAjaxView,
    ResultsDetailByTestView)

urlpatterns = [
    path(
        'summary-by-tests/',
        StatsSummaryByTestView.as_view(active_tab='summary_by_tests'),
        name="summary_by_tests"),
    path(
        'summary-by-tests-ajax/<int:id>/',
        TableStatsAjaxView.as_view(),
        name="summary_by_tests_ajax"),
    path(
        'detailed-by-tests/<int:id>/',
        ResultsDetailByTestView.as_view(),
        name="detailed_by_tests"),
]
