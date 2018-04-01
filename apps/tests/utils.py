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


class TestControllerBase:

    def __init__(self, id, uid, length):
        self.test_id = id
        self.test_uid = uid
        self.current_question_index = 0
        self.lenght = length
        self.answers = []
        self.questions_ids = []

    @staticmethod
    def _get_question(index, question_list):
        for idx, question in enumerate(question_list):
            if idx > index:
                return idx

    def next_question_id(self):
        question = self._get_question(
            self.current_question_index + 1,
            self.questions_ids)
        if question == None:
            question = self.questions_ids[0]
        return question

    def prev_question_id(self):
        question = self._get_question(
            self.current_question_index + 1,
            self.questions_ids)
        if self.question == None:
            question = self.questions_ids[0]
        return question
