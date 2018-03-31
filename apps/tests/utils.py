from django.urls import reverse_lazy

from main.utils import SidebarBaseTabs, SidebarBaseNavs


class SidebarTestTabs(SidebarBaseTabs):
    tabs_list = [
        {
            'title': 'Назначенные тесты',
            'name': 'appointed',
            'url': reverse_lazy('test:appointed'),
            'active': False
        },
        {
            'title': 'Доступные тесты',
            'name': 'available',
            'url': reverse_lazy('test:available'),
            'active': False
        }
    ]


class SidebarTestNavs(SidebarBaseNavs):
    navs_list = [
        {
            'title': 'Админ панель',
            'url': reverse_lazy('admin:index'),
        },
    ]
