from __future__ import absolute_import, unicode_literals

from datetime import timedelta, date, datetime
import pytz
from celery.schedules import crontab
import pandas as pd

from server.celery import app

from aiogram.utils import executor
from accounts.models import Student
from core.models import TimeTable

from core.bot import bot, dp

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=1), schedule_notification.s(), name="schedule_notification"
    )  # Execute daily at midnight.


@app.task(name="schedule_notification")
def schedule_notification():
    allStudent = Student.objects.all()

    for student in allStudent:
        student_id = student.id 
        timezone = pytz.timezone("Europe/Athens")
        
        # get all TimeTable for user for today
        today = datetime.now(timezone).date()
        timeTable = TimeTable.objects.filter(
            group__name=student.group.name, 
            begin__gt=today, 
            end__lte=today + timedelta(days=1)
        )
        
        for i in timeTable:
            begin = i.begin.replace(tzinfo=pytz.utc).astimezone(timezone)
            q = begin - timedelta(minutes=10)

            text = f"{i.abbreviation} в {begin.time()}"
            send_notification.apply_async((student_id, text), eta=q)


@app.task(name="send_notification")
def send_notification(user_id, text):
    executor.start(
        dp, 
        bot.send_message(user_id, text)
    )