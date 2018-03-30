from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/signin.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]
