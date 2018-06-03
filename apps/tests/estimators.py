from django.db.models import IntegerField, Case, When, Count, Sum, Q


class BaseEstimator:

    _result = None

    def __init__(self, test_controller):
        self.test_controller = test_controller
        self.test = self.test_controller.test

    @property
    def result(self):
        if not self._result:
            self._result = self.get_result()
        return self._result

    def get_result(self):

        self.answers_ids = []
        for idx, question in enumerate(self.test_controller):
            self.answers_ids += self.test_controller.get_answer_by_idx(idx)

        result = dict([
            (item['id'], [item['true_count'], item['right_count']])
            for item in self.test.question_set.filter(
                id__in=self.test_controller.get_question_list(),
            ).order_by('id').annotate(
                true_count=Sum(
                    Case(
                        When(
                            answer__is_true=True, then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                ),
                right_count=Sum(
                    Case(
                        When(
                            Q(answer__in=self.answers_ids) & Q(answer__is_true=True),
                            then=1
                        ),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            ).values('id', 'true_count', 'right_count')
        ])

        for idx in range(self.test_controller.length):

            question = self.test_controller._get_question(idx)

            if not isinstance(question, (self.test_controller.non_question_class,)):
                result[question.id].append(
                    len(self.test_controller.get_answer_by_idx(idx)))

        return result

    def estimate(self):
        raise NotImplementedError


class FewInOneEstimator(BaseEstimator):

    def estimate(self):
        score = 0
        result = self.result
        for question in result.values():
            if question[1] == question[2]:

                if question[1] == question[0]:
                    if question[0] < 3:
                        score += 1
                    else:
                        score += 3
                elif question[1] - 1 == question[0]:
                    if question[0] > 2:
                        score += 1
        return score


class OneInOneEstimator(BaseEstimator):

    def estimate(self):
        score = 0
        result = self.result
        for question in result.values():
            if question[1] == question[2]:
                if question[1] == question[0]:
                    score += 1

        return score
