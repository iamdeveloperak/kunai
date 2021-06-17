from celery import shared_task
from .track import *

@shared_task
def update_products():
    track()