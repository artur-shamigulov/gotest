from django.urls import path

from main.views import MainView

urlpatterns = [
    path('', MainView.as_view(active_tab='appointed'), name="main"),
]
