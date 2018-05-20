from django.urls import path

from .views import StatsSummaryByTestView, TableStatsAjaxView

urlpatterns = [
    path(
        'summary-by-tests/',
        StatsSummaryByTestView.as_view(active_tab='summary_by_tests'),
        name="summary_by_tests"),
    path(
        'summary-by-tests-ajax/<int:id>/',
        TableStatsAjaxView.as_view(),
        name="summary_by_tests_ajax"),
]
