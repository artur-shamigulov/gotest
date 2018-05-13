from django.urls import path

from .views import (
	ApointedTestListView, AvailableTestListView,
	StartAvailableTestView, TestView)

urlpatterns = [
    path('appointed/', ApointedTestListView.as_view(active_tab='appointed'), name="appointed"),
    path('available/', AvailableTestListView.as_view(active_tab='available'), name="available"),
    path('available/test/start/<str:slug>/', StartAvailableTestView.as_view(), name="start_available_test"),
    path('test/<str:uuid>/<int:page>/', TestView.as_view(), name="test"),
]
