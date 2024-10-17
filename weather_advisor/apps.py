from django.apps import AppConfig
from django.db.models.signals import post_migrate
from weather_advisor.utils import sync_temperature_data



class WeatherAdvisorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_advisor'


    def ready(self):
        from .tasks import schedule_temperature_data_task
        """Override this method to execute code when the app is ready."""
        # Register signals or perform other startup code
        sync_temperature_data()
        schedule_temperature_data_task()