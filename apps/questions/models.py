from django.db import models

from tests.models import Test


class Question(models.Model):

    test = models.ForeignKey(
        Test, on_delete=models.CASCADE)
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return 'Вопрос #%s' % self.id
