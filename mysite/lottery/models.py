# -*- coding=utf-8 -*-
from django.db import models

# 用户信息表
class UserInfo(models.Model):
	name = models.CharField(max_length=50,unique=True)
	passwd = models.CharField(max_length=50)
	registe_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	class Meta():
		db_table = 'user_info'




class ChongQing_Lottery_Num(models.Model):
	phase = models.CharField(max_length=50,default='')
	time_draw = models.CharField(max_length=50,default='')
	num_data = models.CharField(max_length=50,default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.phase

	class Meta():
		db_table = 'chongqing_num'

#预测一 7位数
class ForecastOne(models.Model):
	phase = models.CharField(max_length=50,default='')
	#预测下期号码
	forecast_code = models.CharField(max_length=50,default='')
	opentime = models.CharField(max_length=50,default='')
	opencode = models.CharField(max_length=50,default='')
	#中奖状态 0 不中  1 中  3 等待开奖
	code = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.phase

	class Meta():
		db_table = 'forecastone'

#遗漏统计
# class LeaveOutStatistics(models.Model):
# 	phase = models.CharField(max_length=50,default='')


#后一七码 增量统计
class MoneyLostOne(models.Model):
	forecastone = models.OneToOneField(ForecastOne)
	put_in_phase = models.CharField(max_length=50,default='')
	opentime = models.CharField(max_length=50,default='')
	put_in_money = models.IntegerField()
	# 0 没中  1中了
	back_status = models.IntegerField()
	back_money = models.IntegerField()

	def __unicode__(self):
		return self.put_in_phase

	class Meta():
		db_table = 'money_lost_one'




#django_test

class Item(models.Model):
    name = models.CharField(max_length=10)
    data = models.IntegerField()
    person = models.ForeignKey('person', null=True, blank=True)
    class Meta:
        ordering = ["name"]

class Person(models.Model):
	age = models.IntegerField()