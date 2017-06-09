
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
		days = dateRange("2017-06-07", "2017-6-10")
		url_list = get_url(days)
		get_html_data(url_list)
		end = time.time()
		print(end-start)
		print('weizhanbiao')


#get time list
def dateRange(start, end, step=1, format="%Y-%m-%d"):
	strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
	days = (strptime(end, format) - strptime(start, format)).days
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
		print(time_draw,data)
		#save history num 
		ChongQing_Lottery_Num.objects.get_or_create(phase = phase,time_draw = time_draw,num_data = data)

		#save forecast num 
		forecase_num_list = [_ for _ in range(10)]
		rm_one = int(phase[-1])
		forecase_num_list.remove(rm_one)
		pre_phase = int(phase) - 1
		try:
			obj = ChongQing_Lottery_Num.objects.get(phase = str(pre_phase))
		except Exception as e:
			# raise e
			continue
		rm_two = int(obj.num_data[2])-1
		if rm_two == -1:
			rm_two = 9
		if rm_two in forecase_num_list:
			forecase_num_list.remove(rm_two)
		else:
			forecase_num_list.remove(forecase_num_list[random.randint(0,8)])
		rm_three =  random.randint(0,9)
		if rm_three in forecase_num_list:
			forecase_num_list.remove(rm_three)
		else:
			forecase_num_list.remove(forecase_num_list[random.randint(0,7)])
		forecase_num = ''.join(map(str,forecase_num_list))
		if data[-1] in forecase_num:
			code = 1
		else:
			code = 0

		if ForecastOne.objects.filter(phase = phase).exists():
			print('%s这期预测过了'%phase)
		else:
			ForecastOne.objects.create(phase = phase,opencode = data,forecast_code = forecase_num,opentime = time_draw,code = code)
			print('%s预测开始'%phase)


