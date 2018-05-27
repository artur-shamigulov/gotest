from django.urls import reverse_lazy
from django.core.cache import cache

from main.utils import SidebarBaseTabs, SidebarBaseNavs
from .estimators import FewInOneEstimator


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
        },
        {
            'title': 'Результаты',
            'name': 'results',
            'url': reverse_lazy('stats:own_stats'),
            'active': False
        }
    ]


class SidebarStaffTabs(SidebarBaseTabs):
    tabs_list = [
        {
            'title': 'Статистика',
            'name': 'statistic',
            'url': reverse_lazy('stats:summary_by_tests'),
            'active': False
        },
    ]


class SidebarTestNavs(SidebarBaseNavs):
    navs_list = [
    ]


class SidebarStaffNavs(SidebarBaseNavs):
    navs_list = [
        {
            'title': 'Админ панель',
            'url': reverse_lazy('admin:index'),
        },
    ]


class NoQuestionBase(object):
    pass


class TestControllerBase:

    estimator_class = FewInOneEstimator
    non_question_class = NoQuestionBase

    def __init__(self, id, uid, length, test, duration):
        self.test_id = id
        self.test_uid = uid
        self.current_question_index = 0
        self.length = length
        self.duration = duration
        self.test = test
        self.test_name = test._get_test_name(self.test_uid)
        self.set_answers_list([None] * length)

    def __iter__(self):
        return iter(self.get_question_list())

    @staticmethod
    def get_question_list_name(test_name):
        return '%s_qustions' % test_name

    def set_question_list(self, q_list):
        cache.set(
            self.get_question_list_name(
                self.test_name),
            q_list,
            timeout=self.duration
        )

    def get_question_list(self):
        return cache.get(
            self.get_question_list_name(
                self.test_name)) or []

    @staticmethod
    def get_answers_list_name(test_name):
        return '%s_answers' % test_name

    def set_answers_list(self, q_list):
        cache.set(
            self.get_answers_list_name(
                self.test_name),
            q_list,
            timeout=self.duration
        )

    def get_answers_list(self):
        return cache.get(
            self.get_answers_list_name(
                self.test_name))

    @staticmethod
    def _get_question_idx(index, start, to):
        for idx in range(start, to, 1):
            if idx > index:
                return idx

    def next_question_id(self):
        idx = self._get_question_idx(
            self.current_question_index,
            0,
            self.length)
        if idx is None:
            idx = 0
        return idx

    def prev_question_id(self):
        idx = self._get_question_idx(
            self.current_question_index * -1,
            self.length * -1,
            1)
        if idx is None:
            idx = (self.length - 1) * -1
        return (idx) * -1

    def _get_question(self, idx):
        NotImplementedError

    def write_to_cache(self):
        cache.set(
            self.test_name,
            self,
            timeout=cache.ttl(self.test_name))

    def set_current_question(self, idx):
        self.current_question_index = idx
        self.write_to_cache()
        return self._get_question(self.current_question_index)

    def next_question(self):
        self.current_question_index = self.next_question_id()
        self.write_to_cache()
        return self._get_question(self.current_question_index)

    def prev_question(self):
        self.current_question_index = self.prev_question_id()
        self.write_to_cache()
        return self._get_question(self.current_question_index)

    def current_question(self):
        return self._get_question(self.current_question_index)

    def set_answer(self, answer):
        answers = self.get_answers_list()
        answers[self.current_question_index] = answer
        self.set_answers_list(answers)

    def get_answer(self):
        return self.get_answers_list()[self.current_question_index]

    def get_answer_by_idx(self, idx):
        return self.get_answers_list()[idx] or []

    def get_estimator(self):
        return self.estimator_class(self)

    def estimate(self):
        estimator = self.get_estimator()
        return estimator.estimate()


class TestControllerRandom(TestControllerBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_questions()

    def _init_questions(self):
        self.set_question_list(list(self.test.question_set.all(
        ).order_by('?')[:self.length].values_list(
            'id', flat=True)))

    def _get_question(self, idx):
        if len(self.get_question_list()) <= idx:
            return self.non_question_class()

        return self.test.question_set.filter(
            id=self.get_question_list()[idx]).prefetch_related(
            'answer_set').first() or self.non_question_class()
