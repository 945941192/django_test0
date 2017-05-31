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
		return self.name

	class Meta():
		db_table = 'chongqing_num'