import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_paper.settings')

app = Celery('news_paper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_mailing_every_monday_8am': {
        'task': 'weekly_mailing',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
    'check_new_every_one_second': {
        'task': 'check_new',
        'schedule': 1
    }
}
