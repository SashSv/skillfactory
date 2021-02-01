from django.apps import AppConfig


class BlogappConfig(AppConfig):
    name = 'blogapp'
    verbose_name = 'Блог'

    def ready(self):
        import blogapp.signals