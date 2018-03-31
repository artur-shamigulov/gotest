from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import SidebarBaseMixin, NavBaseMixin


class MainView(
        LoginRequiredMixin,
        NavBaseMixin,
        SidebarBaseMixin,
        TemplateView):

    template_name = 'main/main.html'
