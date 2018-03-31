class SidebarBaseTabs(object):

    _tabs_list = []

    def __init__(self, *args, **kwargs):
        super().__init__()

    def tabs_list(self, *args, **kwargs):
        return self._tabs_list


class SidebarBaseNavs(object):

    _navs_list = []

    def __init__(self, *args, **kwargs):
        super().__init__()

    def navs_list(self, *args, **kwargs):
        return self._navs_list
