#coding=utf-8
from __future__ import absolute_import, unicode_literals
#python3连接数据库的方式
import pymysql
pymysql.install_as_MySQLdb()



#django_celery 配置
# from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
'''然后你需要导入这个程序在你的项目/项目/ __init__。py模块。这确保了Django启动时加载应用程序,以便@shared_task装饰将使用它:'''
from .celery import app as celery_app

__all__ = ['celery_app']