from django.utils import timezone

from .models import TestLog
from questions.models import QuestionLog
from answers.models import AnswerLog


class BaseLogger:

    @staticmethod
    def write_log(estimator, uuid):
        TestLog.objects.filter(test_uid=uuid).update(
            datetime_completed=timezone.now(),
            score=estimator.estimate())
        test_log = TestLog.objects.get(test_uid=uuid)
        questions = []
        answers = []
        for question in estimator.result:
            instance = QuestionLog(
                test_log=test_log,
                question_id=question
            )
            for answer in estimator.answers_ids:
                if answer.question_id == question:
                    answers.append(AnswerLog(
                        question_log=instance,
                        answer=answer
                    ))
            questions.append(instance)

        QuestionLog.objects.bulk_create(questions)
        for answer in answers:
            answer.question_log_id = answer.question_log.id
        AnswerLog.objects.bulk_create(answers)
