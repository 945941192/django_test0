
#coding=utf-8
import requests
import json
import datetime
import time
import random


from django.core.management.base import BaseCommand, CommandError
from lottery.models import ChongQing_Lottery_Num,ForecastOne

class Command(BaseCommand):
	help = 'wei zhanbiao  zhen shuai qi '



	def handle(self, *args, **options):
		start = time.time()
		#exclude [ limit )
		days = dateRange("2017-06-01", "2017-6-20")
		url_list = get_url(days)
		# judge_forecast_num()
		get_html_data(url_list)
		judge_forecast_num()
		end = time.time()
		print(end-start)
		print('weizhanbiao')


#get time list
def dateRange(start, end, step=1, format="%Y-%m-%d"):
	strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
	days = (strptime(end, format) - strptime(start, format) + datetime.timedelta(days = 1)).days 
	print(days,'*****')
	return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days, step)]

def get_url(days):
	url_list = []
	for day in days:
		url = 'http://baidu.lecai.com/lottery/draw/sorts/ajax_get_draw_data.php?lottery_type=200&date=%s'%day
		url_list.append(url)
	return url_list
def get_html_data(url_list):

	headers = {'Accept':"application/json, text/javascript, */*; q=0.01",
	"Accept-Encoding":"gzip,deflate,sdch",
	"Accept-Language":"zh-CN,zh;q=0.8",
	"Connection":"keep-alive",
	"Cookie":"_source=5555; _source_pid=0; _srcsig=b109a5da; _lhc_uuid=sp_5915b61f51f0f1.67571511; LSID=b1cq21atvrdcr8uc44cicf66v2; _adwp=110406678.1133539953.1494595485.1494595485.1494597860.2; _adwc=110406678; _adwr=110406678%23https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253DmTHdx8YjfvLb_U2XnvCsqvPBmhXcAw9xs6hn6KCP12il-upyhJHhM2eI0yUABKW8Asbe9sgm0eOOslXO_3R24QW2dtJ9G98h8e_MbsZI_Ca%2526wd%253D%2526eqid%253D8e79f57a00051dfc000000035915b614; _adwb=110406678; Hm_lvt_6c5523f20c6865769d31a32a219a6766=1494595485,1494597871,1494597880; Hm_lpvt_6c5523f20c6865769d31a32a219a6766=1494601654; Hm_lvt_9b75c2b57524b5988823a3dd66ccc8ca=1494595485,1494597871,1494597880; Hm_lpvt_9b75c2b57524b5988823a3dd66ccc8ca=1494601654",
	"Host":"baidu.lecai.com",
	"Referer":"http://baidu.lecai.com/lottery/draw/view/200?agentId=5555",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
	"X-Requested-With":"XMLHttpRequest"}

	for url in url_list:
		html_data = requests.get(url,headers=headers)
		data = json.loads(html_data.text)
		lottery_data = data.get('data').get('data')
		# print html_data.status_code,data
		analysys_data(lottery_data)

def analysys_data(lottery_data):
	for obj in lottery_data:
		phase = obj.get('phase')
		time_draw = obj.get('time_draw')
		data =''.join(obj.get('result').get('result')[0].get('data'))
		#save history num 
		ChongQing_Lottery_Num.objects.get_or_create(phase = phase,time_draw = time_draw,num_data = data)
		#保存本期开奖结果
		if ForecastOne.objects.filter(phase = phase).exists():
			if not ForecastOne.objects.get(phase = phase).opencode:
				# print('*'*89)
				wait_update_obj = ForecastOne.objects.get(phase = phase)
				wait_update_obj.opencode = data
				wait_update_obj.save()
				print(('本期%s开奖号码录入'%phase)*9)

		#预测号码
		forecase_num_list = [_ for _ in range(10)]
		#下一期期号
		# import pdb;pdb.set_trace
		nex_phase = nex_phase_hander(phase)
		rm_one = int(nex_phase[-1])
		forecase_num_list.remove(rm_one)
		try:
			obj = ChongQing_Lottery_Num.objects.get(phase=phase)
		except Exception as e:
			raise e
			continue
		#这一期中间号码减一
		rm_two = int(obj.num_data[2])-1
		if rm_two == -1:
			rm_two = 9
		if rm_two in forecase_num_list:
			forecase_num_list.remove(rm_two)
		else:
			forecase_num_list.remove(forecase_num_list[random.randint(0,8)])
		#对称杀
		# rm_three =  random.randint(0,9)
		rm_three = int((ChongQing_Lottery_Num.objects.filter(phase__lte=phase).order_by('-phase')[40]).num_data[-1])
		if rm_three in forecase_num_list:
			forecase_num_list.remove(rm_three)
		else:
			forecase_num_list.remove(forecase_num_list[random.randint(0,7)])
		forecase_num = ''.join(map(str,forecase_num_list))
		code = 3
		#存入下一期预测号码、创建预测对象
		if ForecastOne.objects.filter(phase = nex_phase).exists():
			print('%s这期预测过了'%nex_phase)
			pass
		else:
			ForecastOne.objects.create(phase = nex_phase,opencode = '',forecast_code = forecase_num,opentime = time_draw,code = code)
			print('%s期   ---------  预测号码为 -----------》%s'%(nex_phase,forecase_num))





#获取下一期期数
def nex_phase_hander(phase):
	today_max_phase = phase[0:8]+'120'
	today_min_phase = phase[0:8]+'001'

	if phase == today_max_phase:
		print('max')
		today = datetime.datetime.strptime(phase[0:8],"%Y%m%d")
		nex_day = today + datetime.timedelta(days = 1)
		nex_phase = nex_day.strftime("%Y%m%d") + '001'
		return nex_phase
	else:
		nex_phase = str(int(phase)+1)
		return nex_phase


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


#验证预测号码
def judge_forecast_num():
	#找出code=3的等待开奖的
	print('正在检测预测号码的正确性')
	query_set = ForecastOne.objects.filter(code = 3)
	for obj in query_set:
		phase = obj.phase
		# import pdb;pdb.set_trace()
		# print(obj.phase,obj.forecast_code,'验证正确性的')
		try:
			if obj.opencode[-1] in obj.forecast_code:
				obj.code = 1
				obj.save()
				print('%s期---->预测号码为%s------>开奖号码为%s========正确'%(obj.phase,obj.forecast_code,obj.opencode[-1]))
			else:
				obj.code = 0
				obj.save()
				print('%s期---->预测号码为%s------>开奖号码为%s=====================不正确'%(obj.phase,obj.forecast_code,obj.opencode[-1]))
		except Exception as e:
			# raise e
			pass


#celery use

def celery_spider():
		today = datetime.datetime.now().strftime('%Y-%m-%d')
		tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
		start = time.time()
		days = dateRange(today, tomorrow)
		url_list = get_url(days)
		judge_forecast_num()
		get_html_data(url_list)
		judge_forecast_num()
		end = time.time()
		print('爬取数据所用时间为',end-start)
		print('weizhanbiao','爬取的时间段是%s'%days)







