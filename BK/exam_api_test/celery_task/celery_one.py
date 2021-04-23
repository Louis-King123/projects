# !/usr/bin python3                                 
# encoding    : utf-8 -*-                            
# @author     :   shexiaolong                               
# @software   : PyCharm      
# @file       :   celery_one.py
# @Time       :   2021/4/22 4:51 下午

from celery import task
from blueking.component.shortcuts import get_client_by_user
import time


@task.periodic_task(run_every=5)
def some_task():
    print('每5秒执行一次')
    print('执行完毕')
    return time.localtime()
