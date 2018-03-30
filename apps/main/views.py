from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'main/main.html'
