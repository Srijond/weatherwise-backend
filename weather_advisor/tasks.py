from background_task import background
from background_task.models import Task
from datetime import datetime, timedelta
from django.utils import timezone
from .utils import sync_temperature_data


@background(schedule=600)
def fetch_district_temperature_data():
    print(f"Task is running at: {datetime.now()}")
    sync_temperature_data()
    print(f"Task is finished: {datetime.now()}")


def schedule_temperature_data_task():
    # Schedule the task to run every 6 hours
    if not Task.objects.filter(verbose_name='my_scheduled_task').exists():
        fetch_district_temperature_data(repeat=21600)

