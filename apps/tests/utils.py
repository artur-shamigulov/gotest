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


class NoQuestionBase(object):
    pass


class TestControllerBase:

    def __init__(self, id, uid, length, test):
        self.test_id = id
        self.test_uid = uid
        self.current_question_index = -1
        self.length = length
        self.test = test
        self.answers = []
        self.questions_ids = []

    def _get_question_idx(self, index, question_list):
        for idx in range(self.length):
            if idx > index:
                return idx

    def next_question_id(self):
        idx = self._get_question_idx(
            self.current_question_index,
            self.questions_ids)
        if idx is None:
            idx = 0
        return idx

    def prev_question_id(self):
        idx = self._get_question_idx(
            self.current_question_index,
            self.questions_ids[::-1])
        if idx is None:
            idx = 0
        return idx

    def _get_question(self, idx):
        NotImplementedError

    def next_question(self):
        self.current_question_index = self.next_question_id()
        print(self.current_question_index)
        return self._get_question(self.current_question_index)

    def prev_question(self):
        self.current_question_index = self.prev_question_id()
        return self._get_question(self.current_question_index)


class TestControllerRandom(TestControllerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_questions()

    def _init_questions(self):
        self.questions_ids = list(self.test.question_set.all(
        ).order_by('?')[:self.length].values_list(
            'id', flat=True))
        print(self.questions_ids)

    def _get_question(self, idx):
        if len(self.questions_ids) <= idx:
            return NoQuestionBase()

        return self.test.question_set.filter(
            id=self.questions_ids[idx]).prefetch_related(
            'answer_set').first() or NoQuestionBase()
