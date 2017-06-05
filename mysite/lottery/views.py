#coding=utf-8
import requests
import json
import time



from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from lottery.models import ChongQing_Lottery_Num,ForecastOne

from lottery.management.commands.forecastone import get_html




def ChongQing(request):

	if request.method == "GET":
		return render(request,'lottery/lottery_num_analysis.html')
	else:
		num_data_set = ChongQing_Lottery_Num.objects.all().order_by('-phase')[:600]
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




