from django.conf.urls import url
from . import views
from lottery.views import LotteryLastOne

#
from django.views.generic import TemplateView

urlpatterns = [
	#通用视图函数
    url(r'^lottery/chongqing$', views.ChongQing, name='chongqing'),
    url(r'^lottery/realtimedata',views.RealTimeDate,name='realtimedata'),
    url(r'^lottery/forecastone',views.ForecastOneHandle,name='forecastone'),
    url(r'^lottery/last1',views.LastOneHandle,name='lotterylast1'),

    #基于类的视图
    url(r'^lottery/about/', TemplateView.as_view(template_name='lottery/lottery_num_analysis.html')),
    url(r'^lottery/last_one/', LotteryLastOne.as_view()),

]
