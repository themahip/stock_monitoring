import os
from celery import Celery
from celery.schedules import crontab
from .settings import TIME_ZONE

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('ramailo')
app.conf.timezone = TIME_ZONE


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks([
    "stock.tasks.stock_tasks"
])

app.conf.broker_transport_options = {
    'max_retries': 2,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

app.conf.beat_schedule = {
    'execute_ramailo_task_in_every_2_min': {
        'task': 'execute_stock_task',
        'schedule': 1 * 60   # Run every 2 min
    },
}