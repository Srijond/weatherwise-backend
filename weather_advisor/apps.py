from django.apps import AppConfig
from django.db.models.signals import post_migrate
from weather_advisor.utils import handle


class WeatherAdvisorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_advisor'


    def ready(self):
        """Override this method to execute code when the app is ready."""
        # Register signals or perform other startup code
        flag = False
        if flag:
            print('hello 1st srijon-----')
            self.perform_initial_setup()
            flag = False
        

    def perform_initial_setup(self):
        handle()
        
