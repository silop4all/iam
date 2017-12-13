from django.apps import AppConfig

class IamAppConfig(AppConfig):
    name = 'app'
    verbose_name = "IAM"

    def ready(self):
        # import signal handlers
        import app.signals