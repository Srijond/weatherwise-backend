from background_task import background
from background_task.models import Task
from datetime import datetime, timedelta
from django.utils import timezone
from .utils import sync_temperature_data


@background(schedule=600)
def my_scheduled_task():
    print(f"Task is running at: {datetime.now()}")
    sync_temperature_data()
    print(f"Task is finished: {datetime.now()}")


def schedule_test_task():
    # Schedule the task to run every 6 hours
    if not Task.objects.filter(verbose_name='my_scheduled_task').exists():
        my_scheduled_task(repeat=21600)

