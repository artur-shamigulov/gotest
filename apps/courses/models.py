from django.db import models


class Course(models.Model):

    title = models.CharField('Название', max_length=255)
    slug = models.SlugField('Slug')

    def __str__(self):
        return self.title
