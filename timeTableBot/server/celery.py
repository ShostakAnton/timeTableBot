from __future__ import absolute_import

import os
import warnings

from django.conf import settings

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

broker = 'redis://redis-timeTableBot:6379/0'
app = Celery("server", broker=broker)

app.config_from_object("django.conf:settings", namespace='CELERY')
app.conf.imports = (
    "core.tasks",
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
    
warnings.filterwarnings("ignore")

@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request), flush=True)