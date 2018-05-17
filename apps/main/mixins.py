from django.utils import timezone

from tests.utils import (
    SidebarTestTabs, SidebarTestNavs,
    SidebarStaffNavs, SidebarStaffTabs
)
from tests.models import TestLog


class SidebarBaseMixin(object):

    active_tab = None

    def tabs_list_factory(self):
        if self.request.user.is_staff:
            return SidebarStaffTabs(self)
        return SidebarTestTabs(self)

    def tabs_list(self, **kwargs):

        tabs = self.tabs_list_factory().get_tabs(self)

        for tab in tabs:
            if tab['name'] == self.active_tab:
                tab['active'] = True
        return tabs

    def current_test(self, **kwargs):
        now = timezone.now()
        return TestLog.objects.filter(
            datetime_created__lte=now,
            datetime_completed__gt=now,
            user=self.request.user)


class NavBaseMixin(object):

    def navs_list_factory(self):
        if self.request.user.is_staff:
            return SidebarStaffNavs(self)
        return SidebarTestNavs(self)

    def navs_list(self, **kwargs):
        return self.navs_list_factory().get_navs(self)
