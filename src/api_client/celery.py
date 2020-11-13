import os
from decimal import Decimal

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testing_app.settings')

app = Celery('testing_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()