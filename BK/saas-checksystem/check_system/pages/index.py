# -*- coding: utf-8 -*-
import time
from django.shortcuts import render
from check_system.common.notify import send_notify
from check_system.common.request import Request
from blueking.component.shortcuts import get_client_by_request

def index(request):
    return render(request, "index.html")

def login_username(request):
    """
    @request
    获取登录用户名
    """
    sys_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    username = request.user.username

    return Request.succFcun("hello world", data={"user":username, "time": sys_time})

def bk_users(request):
    client = get_client_by_request(request)
    kwargs={
        "fields": "username,id",
        "no_page": True
    }
    res= client.usermanage.list_users(kwargs)
    return Request.succFcun("sucess", data=res['data'])