#coding=utf-8

#common
import requests
import json
import time
import datetime

#django
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from lottery.models import ChongQing_Lottery_Num,ForecastOne

#view generic
from django.views.generic import View,ListView

#spider
from lottery.management.commands.forecastone import get_html

#celery
from lottery.tasks import lottery_spider




def ChongQing(request):

	if request.method == "GET":
		return render(request,'lottery/lottery_num_analysis.html')
	else:
		num_data_set = ChongQing_Lottery_Num.objects.all().order_by('-phase')[:30]
		list_all = []

		for obj in num_data_set:
			list_all.append(obj.num_data)
		num_30 = ','.join(list_all)
		one_num = num_30.count('1')
		two_num = num_30.count('2')
		three_num = num_30.count('3')
		four_num = num_30.count('4')
		five_num = num_30.count('5')
		six_num = num_30.count('6')
		seven_num = num_30.count('7')
		eight_num = num_30.count('8')
		nine_num = num_30.count('9')
		zreo_num = num_30.count('0')
		print(zreo_num,'%'*80)
		data = {'one_num':one_num,'two_num':two_num,'three_num':three_num,'four_num':four_num,'five_num':five_num,'six_num':six_num,'seven_num':seven_num,'eight_num':eight_num,'nine_num':nine_num,'zreo_num':zreo_num}

		print(one_num) 
		return JsonResponse(data)


def RealTimeDate(request):
	if request.method == 'GET':
		html_data = requests.get('http://f.apiplus.net/cqssc-50.json')
		if html_data.status_code == 200:
			context = json.loads(html_data.text)
		else:
			return HttpResponse('api erro')
		return render(request,'lottery/lottery_realtime_data.html',context)

def ForecastOneHandle(request):
	if request.method == 'GET':
		# get_html()
		#forecash_set = ForecastOne.objects.filter(opentime__gt= '2017-06-04 00:00:00').order_by('-phase')
		lottery_spider.delay()
		forecash_set = ForecastOne.objects.all()
		count1 = forecash_set.filter(code=1).count()
		count2 = forecash_set.count()-count1
		return render(request,'lottery/lottery_forecast_one.html',{'forecash_set':forecash_set,'count1':count1,'count2':count2})


def LastOneHandle(request):
	if request.method == 'GET':
		# queryset = list(ChongQing_Lottery_Num.objects.filter(time_draw__gt='2017-06-07 00:00:00').order_by('phase'))
		queryset = list(ChongQing_Lottery_Num.objects.filter(time_draw__gt='2017-00-00 00:00:00').order_by('phase'))

		#针对不同数字对一个的遗漏对象集合
		zreo_obj_list = list()
		# zreo_obj_list = list()

		#当前遗漏值
		recently_lost_data = dict()
		#后一为 0 的queryset集合
		for obj in queryset:
			if obj.num_data[-1] == '0':
				zreo_obj_list.append(obj)

		for index,obj in enumerate(zreo_obj_list):
			if index == 0:
				obj.lost_num = 0
			else:
				obj.lost_num = queryset.index(obj) - queryset.index(zreo_obj_list[index-1]) - 1
			print(obj.phase,'-----000000--->遗漏期数',obj.lost_num)
		
		lost_num_list = [i.lost_num for i in zreo_obj_list]
		print(lost_num_list,'-------最大遗漏为-------》',max(lost_num_list))
		return render(request,'lottery/lottery_last1.html')
	else:
		queryset = list(ChongQing_Lottery_Num.objects.filter(time_draw__gt='2017-06-07 00:00:00').order_by('phase'))[-100:]
		list_all = list()
		for obj in queryset:
			list_all.append(obj.num_data[-1])
		one_num = list_all.count('1')
		two_num = list_all.count('2')
		three_num = list_all.count('3')
		four_num = list_all.count('4')
		five_num = list_all.count('5')
		six_num = list_all.count('6')
		seven_num = list_all.count('7')
		eight_num = list_all.count('8')
		nine_num = list_all.count('9')
		zreo_num = list_all.count('0')
		data = {'one_num':one_num,'two_num':two_num,'three_num':three_num,'four_num':four_num,'five_num':five_num,'six_num':six_num,'seven_num':seven_num,'eight_num':eight_num,'nine_num':nine_num,'zreo_num':zreo_num}
		return JsonResponse(data)


class LotteryLastOne(View):
	def get(self,request):
		return HttpResponse('hello Views')




