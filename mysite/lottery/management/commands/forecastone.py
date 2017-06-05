
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
	help = 'wei zhanbiao  zhen shuai qi '



	def handle(self, *args, **options):
		try:
			get_html()
		except Exception as e:
			time.time(2)
			get_html()



def get_html():
	try:
		html_data = requests.get('http://f.apiplus.net/cqssc-50.json',timeout=2)
		if html_data.status_code == 200:
			context = json.loads(html_data.text)
			for index,obj in enumerate(context['data']):
				if index <= 10:
					opencode = ''.join(obj['opencode'].split(','))
					# ChongQing_Lottery_Num.objects.get_or_create(phase = obj['expect'],num_data = opencode)

					# forecastone Do
					forecase_num_list = [_ for _ in range(10)]
					# 期号 中间号  还有对称号
					rm_one = int(obj['expect'][-1])
					forecase_num_list.remove(rm_one)
					rm_two = int(''.join(context['data'][index+1]['opencode'].split(','))[-3])-1
					if rm_two == '-1':
						rm_two = '9'
					if rm_two in forecase_num_list:
						forecase_num_list.remove(rm_two)
					else:
						forecase_num_list.remove(forecase_num_list[random.randint(0,8)])
					rm_three =  random.randint(0,9)
					if rm_three in forecase_num_list:
						forecase_num_list.remove(rm_three)
					else:
						forecase_num_list.remove(forecase_num_list[random.randint(0,7)])
					# print(index,obj,forecase_num_list,len(forecase_num_list))
					forecase_num = ''.join(map(str,forecase_num_list))
				
					if obj['opencode'][-1] in forecase_num:
						code = 1
					else:
						code = 0

					print(obj['opencode'][-1],forecase_num,code)
					opentime = obj['opentime']
					if ForecastOne.objects.filter(phase = obj['expect']).exists():
						print('这期预测过了')
					else:
						ForecastOne.objects.create(phase = obj['expect'],opencode = opencode,forecast_code = forecase_num,opentime = opentime,code = code)
						print('预测开始')
	except Exception as e:
		time.sleep(0.5)
		get_html()				
