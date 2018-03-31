from tests.utils import SidebarTestTabs, SidebarTestNavs


class SidebarBaseMixin(object):

    active_tab = None

    def tabs_list_factory(self):
        return SidebarTestTabs(self)

    def tabs_list(self, **kwargs):

        tabs = self.tabs_list_factory()

        for tab in tabs.tabs_list(self):
            if tab['name'] == self.active_tab:
                tab['active'] = True
        return tabs.tabs_list(self)


class NavBaseMixin(object):

    def navs_list_factory(self):
        return SidebarTestNavs(self)

    def navs_list(self, **kwargs):
        return self.navs_list_factory().navs_list(self)
