from django.urls import path

from .views import ApointedTestListView, AvailableTestListView

urlpatterns = [
    path('appointed/', ApointedTestListView.as_view(active_tab='appointed'), name="appointed"),
    path('available/', AvailableTestListView.as_view(active_tab='available'), name="available"),
]
