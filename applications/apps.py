from django.apps import AppConfig


class ApplicationsConfig(AppConfig):
    name = 'applications'
    verbose_name = 'Applications'

    def ready(self):
        pass