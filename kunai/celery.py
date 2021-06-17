from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta
from celery import Celery
# from django.conf import settings
# from django.apps import apps

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kunai.settings')

celery_app = Celery('kunai')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf.settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

celery_app.conf.beat_schedule = {
    'update-product':{
        'task': 'tracker.tasks.update_products',
        'schedule': timedelta(minutes=5),
    }
}