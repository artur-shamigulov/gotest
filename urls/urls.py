from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        'accounts/',
        include(('accounts.urls', 'accounts'), namespace='account'),
    ),
    path('admin/', admin.site.urls),
    path('test/', include(('tests.urls', 'tests'), namespace='test')),
    path('stats/', include(('stats.urls', 'stats'), namespace='stats')),
    path('', include(('main.urls', 'main'), namespace='main')),
]
