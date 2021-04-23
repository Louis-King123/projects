# -*- coding: utf-8 -*-
from datetime import timezone

from celery.schedules import crontab

from blueapps.core.celery.celery import app
from django_celery_beat.tzcrontab import TzAwareCrontab



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
            crontab(hour=7, minute=30, day_of_week=1,tz=timezone.get_current_timezone()),
        test.s('Happy Mondays!'),
    )


@app.task()
def test(args):
    print(args)












