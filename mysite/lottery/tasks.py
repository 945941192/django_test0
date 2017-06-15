#coding=utf-8
# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

#import spider
from lottery.management.commands.lottery_spider import celery_spider


@shared_task
def lottery_spider():
    celery_spider()



