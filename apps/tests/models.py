from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

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

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title


class AppointedTestQuerySet(models.QuerySet):

    def future(self, **kwargs):
        kwargs['datetime_end__gte'] = timezone.now()

        return self.filter(**kwargs)


class AppointedTestManager(models.Manager):

    def future(self, **kwargs):
        return self.get_queryset().future(**kwargs)

    def get_queryset(self):
        return AppointedTestQuerySet(self.model, using=self._db)


class AppointedTest(models.Model):

    title = models.CharField(
        'Заголовок', default='Назначенный тест', max_length=255)
    users = models.ManyToManyField(User, verbose_name='Пользователи')
    tests = models.ManyToManyField(Test, verbose_name='Тесты')
    duration = models.PositiveSmallIntegerField('Длительность', default=60)
    datetime_start = models.DateTimeField('Начало теста')
    datetime_end = models.DateTimeField('Окончание теста')

    objects = AppointedTestManager()

    class Meta:
        verbose_name = 'Назначенный тест'
        verbose_name_plural = 'Назначенные тесты'

    @property
    def is_available(self):
        now = timezone.now()

        return (
            self.datetime_start <= now and
            self.datetime_end > now)

    def __str__(self):
        return '%s %s-%s' % (
            self.title, self.datetime_start, self.datetime_end)


class AvailableTest(models.Model):

    title = models.CharField(
        'Заголовок', default='Доступный тест', max_length=255)
    users = models.ManyToManyField(User, verbose_name='Пользователи')
    tests = models.ManyToManyField(Test, verbose_name='Тесты')

    class Meta:
        verbose_name = 'Доступный тест'
        verbose_name_plural = 'Доступные тесты'

    def __str__(self):
        return self.title
