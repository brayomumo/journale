import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journale.config.settings')

app = Celery('journale')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


from celery.schedules import crontab
from datetime import datetime

CELERY_BEAT_SCHEDULE = { 
    'Task_one_schedule' : { 
        'task': 'journale.journal.task.send_journals', 
        'schedule': crontab(hour=12), # Run every 12pm
    }
}