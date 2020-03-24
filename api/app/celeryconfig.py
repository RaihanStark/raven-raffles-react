from celery.schedules import crontab


CELERY_IMPORTS = ('app.raffle.util')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'app.raffle.util.refresh_raffles',
        # Execute every three hours: midnight, 3am, 6am, 9am, noon, 3pm, 6pm, 9pm.
        'schedule': crontab(minute=0, hour='*/3'),
    }
}
