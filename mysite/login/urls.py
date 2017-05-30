from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    # url(r'^is_username_exists/$', views.is_username_exists,
    #     name='is_username_exists'),
    # url(r'^is_email_exists/$', views.is_email_exists, name='is_email_exists'),
    # url(r'^registerHandler/$', views.registerHandler, name='registerHandler'),
    # url(r'^loginHandler/$', views.loginHandler, name='loginHandler'),
    # url(r'^logout/$', views.logout, name='logout'),
]
