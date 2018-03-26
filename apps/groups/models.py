from django.db import models
from django.contrib.auth.models import User


class UserGroup(models.Model):

    title = models.CharField(
        'Заголовок', max_length=255)
    users = models.ManyToManyField(User, verbose_name='Пользователи')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title
