from django.apps import AppConfig


class RestbucksConfig(AppConfig):
    name = 'restbucks'

    def ready(self):
        import restbucks.signals  # for call signal decorators
