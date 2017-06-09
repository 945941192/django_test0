#coding=utf-8
import requests
import json
import time
import datetime


from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from lottery.models import ChongQing_Lottery_Num,ForecastOne

from lottery.management.commands.forecastone import get_html




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
		get_html()
		forecash_set = ForecastOne.objects.filter(opentime__gt= '2017-06-04 00:00:00').order_by('-phase')
		count1 = forecash_set.filter(code=1).count()
		count2 = forecash_set.count()-count1
		return render(request,'lottery/lottery_forecast_one.html',{'forecash_set':forecash_set,'count1':count1,'count2':count2})


def LastOneHandle(request):
	if request.method == 'GET':
		queryset = list(ChongQing_Lottery_Num.objects.filter(time_draw__gt='2017-06-07 00:00:00').order_by('phase'))[-100:]
		#最近一期的期数
		# big_num = -1
		# small_num = -2
		recently_phase = queryset[-1]
		# pre_phase = queryset[small_num]
		# n = 0
		# m = 0
		n_0 = 0
		if recently_phase.num_data[-1] == 0:
			small_num = -2
			n = 0
			if recently_phase.num_data[-1] == queryset[small_num]:
				n = 0
				small_num+=1
			else:


		
		return HttpResponse('hello')
		# return render(request,'lottery/lottery_last1.html')
	else:
		# queryset = list(ChongQing_Lottery_Num.objects.filter(time_draw__gt='2017-06-07 00:00:00').order_by('phase'))[-100:]
		# list_all = list()
		# for obj in queryset:
		# 	list_all.append(obj.num_data[-1])
		# one_num = list_all.count('1')
		# two_num = list_all.count('2')
		# three_num = list_all.count('3')
		# four_num = list_all.count('4')
		# five_num = list_all.count('5')
		# six_num = list_all.count('6')
		# seven_num = list_all.count('7')
		# eight_num = list_all.count('8')
		# nine_num = list_all.count('9')
		# zreo_num = list_all.count('0')
		# data = {'one_num':one_num,'two_num':two_num,'three_num':three_num,'four_num':four_num,'five_num':five_num,'six_num':six_num,'seven_num':seven_num,'eight_num':eight_num,'nine_num':nine_num,'zreo_num':zreo_num}

		#遗漏数
		omit_number_zreo = 0
		omit_number_one = 0 
		omit_number_two = 0
		omit_number_three = 0
		omit_number_four = 0
		omit_number_five = 0
		omit_number_six = 0
		omit_number_seven = 0
		omit_number_eight = 0
		omit_number_night = 0
		
		#最近一期的期数
		big_num = -1
		small_num = -2
		recently_phase = queryset[big_num]
		pre_phase = queryset[small_num]
		n = 0
		m = 0
		while n<1:
			if recently_phase.num_data[-1] == pre_phase.num_data[-1]:
				n+=1
			else:
				big_num -= 1
				small_num -= 1
				m+=1
		print(m,"nihao")
		return HttpResponse('hello')
		# return JsonResponse(data)


