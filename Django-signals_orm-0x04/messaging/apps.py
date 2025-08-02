from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        # Import signal handlers to ensure they're registered when the app is ready
        import messaging.signals

