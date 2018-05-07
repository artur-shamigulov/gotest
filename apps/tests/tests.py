from random import random, randint

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Test, TestLog
from .utils import NoQuestionBase
from questions.models import Question
from answers.models import Answer


class TestRandomTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', password='123')
        test = Test.objects.create(
            title='ТЕСТ',
            slug='test',
            description='empty',
            estimate_method=Test.ESTIMATE_METHODS[0][0]
        )
        for idx in range(20):
            question = Question.objects.create(
                test=test,
                text='Вопрос %s' % idx
            )
            answers = []
            for a_idx in range(4):
                answers.append(
                    Answer(
                        text='Ответ %s' % a_idx,
                        is_true=random() > 0.5,
                        question=question))
            Answer.objects.bulk_create(answers)

    def test_random_test(self):
        test = Test.objects.first()
        item = test.start_test(self.user, 60, 25)
        test = Test.get_test(item.test_uid)
        for i in range(30):
            question = test.next_question()
            self.assertEqual(
                isinstance(question, (NoQuestionBase, Question)),
                True
            )

        test = Test.get_test(item.test_uid)
        for i in range(25):
            test.next_question()
            if isinstance(test._get_question(i), (Question,)):
                test.set_answer(
                    list(
                        test._get_question(i).answer_set.filter(
                            is_true=i < 13
                        ).values_list('id', flat=True)
                    )
                )

        Test.end_test(item.test_uid)
        print (TestLog.objects.first().__dict__)
