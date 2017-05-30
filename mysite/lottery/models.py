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
