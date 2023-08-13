import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'journale.config.settings')

app = Celery('journale')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()