
#coding=utf-8
import requests
import json
import datetime
import time
import random
import time


from django.core.management.base import BaseCommand, CommandError
from lottery.models import ChongQing_Lottery_Num,ForecastOne

class Command(BaseCommand):
	help = '获取每个位置上的遗漏值'


	def handle(self, *args, **options):



# def get_
# 		