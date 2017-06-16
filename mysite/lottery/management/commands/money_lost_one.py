
#coding=utf-8
import requests
import json
import datetime
import time
import random
import time


from django.core.management.base import BaseCommand, CommandError
from lottery.models import ChongQing_Lottery_Num,ForecastOne,MoneyLostOne

class Command(BaseCommand):
	help = 'wei zhanbiao  zhen shuai qi '



	def handle(self, *args, **options):
		save_money_lost_one_data()
		open_status()


#将预测的号码进行判断和加注
def save_money_lost_one_data():
	queryset = ForecastOne.objects.all().filter(opentime__gt= '2017-06-04 00:00:00').order_by('phase')
	print(queryset.count())
	for obj in queryset:
		phase = obj.phase
		pre_phase = pre_phase_hander(phase)
		#上一期中了这一期才下注
		if ForecastOne.objects.filter(phase=pre_phase).exists():
			if ForecastOne.objects.get(phase=pre_phase).code == 1:
				if not MoneyLostOne.objects.filter(put_in_phase=phase).exists():
					money_obj = MoneyLostOne()
					money_obj.put_in_phase = phase
					money_obj.opentime = obj.opentime
					money_obj.put_in_money = 140
					money_obj.back_status = 0
					money_obj.back_money = -140
					#保证预测的那期要存在
					if ForecastOne.objects.filter(phase=phase).exists():
						money_obj.forecastone = ForecastOne.objects.get(phase=phase)
					money_obj.save()
					print('%s--------投入---140--------'%phase)

#根据开奖状态  存储 加注开奖状态和回报
def open_status():
	#这里不太好  每次执行要统统更新一遍
	MoneyLostOne.objects.filter(forecastone__code = 1).update(back_status=1,back_money = 55)
	print('更新买入状态')











#获取上一期期数
def pre_phase_hander(phase):
	today_min_phase = phase[0:8]+'001'
	if phase == today_min_phase:
		today = datetime.datetime.strptime(phase[0:8],"%Y%m%d")
		pre_day = today - datetime.timedelta(days = 1)
		pre_phase = pre_day.strftime("%Y%m%d") + '120'
		return pre_phase
	else:
		pre_phase = str(int(phase)-1)
		return pre_phase
