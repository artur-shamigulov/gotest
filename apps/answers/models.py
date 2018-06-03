from django.db import models

from questions.models import Question, QuestionLog


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)
    text = models.TextField('Ответ')
    is_true = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.text[:20]


class AnswerLog(models.Model):
    question_log = models.ForeignKey(
        QuestionLog, on_delete=models.CASCADE)
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лог ответов'
        verbose_name_plural = 'Логи ответов'
