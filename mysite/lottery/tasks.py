#coding=utf-8
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

#import spider
from lottery.management.commands.lottery_spider import celery_spider


import datetime


@shared_task
def lottery_spider():
    celery_spider()



@shared_task
def crontab_test():
    with open('/Users/wzb/Desktop/crontab_test.txt','a') as f:
    	f.write('hello%s\n'%datetime.datetime.now().strftime('%Y-%m-%d'))
