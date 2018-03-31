from django.urls import reverse_lazy

from main.utils import SidebarBaseTabs, SidebarBaseNavs


class SidebarTestTabs(SidebarBaseTabs):
    _tabs_list = [
        {
            'title': 'Назначенные тесты',
            'name': 'appointed',
            'url': '#',
            'active': False
        },
        {
            'title': 'Доступные тесты',
            'name': 'available',
            'url': '#',
            'active': False
        }
    ]


class SidebarTestNavs(SidebarBaseNavs):
    _navs_list = [
        {
            'title': 'Админ панель',
            'url': reverse_lazy('admin:index'),
        },
    ]
