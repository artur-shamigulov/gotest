from django.db import models

from courses.models import Course


class Test(models.Model):

    ESTIMATE_METHODS = (
        ('default', 'Стандартный'),
        ('many_answers', 'Множество ответов'),
    )

    course = models.ManyToManyField(Course)
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('Slug')
    description = models.TextField('Описание')
    estimate_method = models.CharField(
        'Метод оценки', choices=ESTIMATE_METHODS, max_length=50)
    duration = models.PositiveSmallIntegerField('Длительность', default=60)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title
