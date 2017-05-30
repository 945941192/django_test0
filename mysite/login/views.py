#coding=utf-8
from django.shortcuts import render, redirect
from django.http import *
from lottery.models import UserInfo
from django.core.urlresolvers import reverse
import json
from datetime import datetime

# Create your views here.



def login(request):
    if request.method == 'GET':
        username = request.session.get('r_username',default='')
        # print username,"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO`"
        dic={
        'username':username
        }
        print(dic,'*'*20)
        return render(request, 'html/login.html', dic)
    else:
        name = request.POST.get('name','')
        password = request.POST.get('password','')
        if UserInfo.objects.filter(name = name).exists():
            pw = UserInfo.objects.get(name = name).passwd
        if password == pw:
            return render(request,'index.html')
        return HttpResponse('hello')
