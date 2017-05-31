from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lottery/chongqing$', views.ChongQing, name='chongqing'),
]
