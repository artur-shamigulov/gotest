import copy


class SidebarBaseTabs(object):

    tabs_list = []

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._tabs_list = copy.deepcopy(self.tabs_list)

    def get_tabs(self, *args, **kwargs):
        return self._tabs_list


class SidebarBaseNavs(object):

    navs_list = []

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._navs_list = copy.deepcopy(self.navs_list)

    def get_navs(self, *args, **kwargs):
        return self._navs_list
