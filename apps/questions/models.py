from django.db import models

from tests.models import Test, TestLog


class Question(models.Model):

    test = models.ForeignKey(
        Test, on_delete=models.CASCADE)
    text = models.TextField('Текст')
    klass = models.CharField('Класс вопроса',
                             max_length=255,
                             null=True,
                             blank=True)
    points_amount = models.PositiveSmallIntegerField('Количество баллов',
                                                     default=1)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return 'Вопрос #%s' % self.id


class QuestionLog(models.Model):
    test_log = models.ForeignKey(
        TestLog, on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лог вопросов'
        verbose_name_plural = 'Логи вопросов'
