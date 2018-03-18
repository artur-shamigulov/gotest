from django.db import models

from questions.models import Question


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
