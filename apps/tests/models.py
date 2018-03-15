from django.db import models

from apps.courses.models import Course


class Test(models.Model):

    ESTIMATE_METHODS = (
        ('default', 'Стандартный'),
        ('many_answers', 'Множество ответов'),
    )

    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('Slug')
    description = models.TextField('Описание')
    estimate_method = models.CharField(
        'Метод оценки', choices=ESTIMATE_METHODS, max_length=50)
    duration = models.PositiveSmallIntegerField('Длительность', default=60)

    def __str__(self):
        return self.title
