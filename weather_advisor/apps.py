from django.apps import AppConfig
from django.db.models.signals import post_migrate
from weather_advisor.utils import handle


class WeatherAdvisorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_advisor'


    def ready(self):
        """Override this method to execute code when the app is ready."""
        # Register signals or perform other startup code
        if not hasattr(self, 'already_handled'):
            from weather_advisor.utils import handle
            # handle()
            self.already_handled = True
        
