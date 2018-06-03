from django.apps import AppConfig


class TestsConfig(AppConfig):
    name = 'tests'
    verbose_name = 'Тесты'

    def ready(self):
        from .models import Test
        from .logger import BaseLogger

        Test.set_logger(BaseLogger)
