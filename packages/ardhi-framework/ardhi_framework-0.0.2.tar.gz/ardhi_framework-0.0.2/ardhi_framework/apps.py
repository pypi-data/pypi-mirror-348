from django.apps import AppConfig


class RestFrameworkConfig(AppConfig):
    name = 'ardhi_framework'
    verbose_name = "Ardhi Lands framework"

    def ready(self):
        # Add System checks
        ...