from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lottery/chongqing$', views.ChongQing, name='chongqing'),
    url(r'^lottery/realtimedata',views.RealTimeDate,name='realtimedata'),
    url(r'^lottery/forecastone',views.ForecastOneHandle,name='forecastone'),
    url(r'^lottery/last1',views.LastOneHandle,name='lotterylast1'),
]
