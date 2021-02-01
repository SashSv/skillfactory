import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djblog.settings')

app = Celery('djblog')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_every_2_min': {
        'task': 'blogapp.tasks.send_letters_to_all_subscribers',
        'schedule': crontab(minute='*/2'),
    },
}
