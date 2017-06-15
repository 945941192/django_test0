#coding=utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django.conf import settings



'''set the default Django settings module for the 'celery' program.
	设置环境变量（让celery找到dajngo项目）'''
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')


''' 这个app就是celery的实例'''
app = Celery('mysite')

''' Using a string here means the worker don't have to serialize
the configuration object to child processes.
- namespace='CELERY' means all celery-related configuration keys
should have a `CELERY_` prefix.'''
#将settings对象作为参数传入
app.config_from_object('django.conf:settings',)

'''  Load task modules from all registered Django app configs. '''
#celery 自动发现这些模块
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

