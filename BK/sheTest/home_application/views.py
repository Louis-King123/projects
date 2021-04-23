# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.shortcuts import render
from django.http import JsonResponse
import datetime
import uuid
import json
from blueking.component.shortcuts import get_client_by_request
from home_application.models import History, Logs
from celery_mission import log_result
from django.core.paginator import Paginator


SYSTEM_DICT = {
    '1': 'Linux',
    '2': 'Windows',
    '3': 'AIX'
}


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

def home_index(request):
    """
    首页
    """
    return render(request, 'home_application/home_index.html')


def history(request):
    """
    首页
    """

    return render(request, 'home_application/history.html')


def api_test(request):
    """
    首页
    """
    return JsonResponse({"message": "hello world",
                         "data":
                             {"user": request.user.username,
                              "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                         "result": "true"})


def all_business(request, d=None):
    """
    获取所有业务
    """
    client = get_client_by_request(request)
    date = {
        "fields": [
            "bk_biz_id",
            "bk_biz_name"
        ]
    }
    result = client.cc.search_business(date)
    if d:
        return result['data']['info']
    return JsonResponse({"data": result['data']['info']})


def job_list(request):
    """
    作业模版详情
    """
    biz_id = request.GET.get('biz_id', '')
    client = get_client_by_request(request)
    date = {
        "bk_biz_id": biz_id,
    }
    result = client.job.get_job_plan_list(date)
    return JsonResponse({"data": result['data']})


def list_biz_hosts(request):
    """
    查询主机
    """
    biz_id = request.GET.get('biz_id', '')
    client = get_client_by_request(request)
    date = {
        "bk_biz_id": biz_id,
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_id"
        },
        "fields": [
            "bk_host_id",
            "bk_host_name",
            "bk_host_innerip",
            "bk_os_type",
            "bk_cpu",  # cpu核心数
            "bk_mem",  # 内存容量
            "bk_disk",  # 磁盘容量
            "bk_os_version"
        ]
    }
    result = client.cc.list_biz_hosts(date)
    if result['data']:
        infos = result['data']['info']
        for info in infos:
            info['bk_os_type'] = SYSTEM_DICT[info['bk_os_type']]
    return JsonResponse({"data": result['data']['info'] if len(result['data']) > 0 else []})


def job_detail(request):
    biz_id = request.GET.get('biz_id', '')
    job_id = request.GET.get('job_id', '')
    date = {
        "bk_biz_id": biz_id,
        "job_plan_id": job_id
    }
    client = get_client_by_request(request)
    result = client.job.get_job_plan_detail(date)
    return result


def execute_job(request):
    detail = job_detail(request)
    global_lists = detail['data']['global_var_list']

    biz_id = request.GET.get('biz_id', '')
    job_id = request.GET.get('job_id', '')
    hosts = request.GET.get('hosts', '')

    var_server = {}
    ip_lists = [{"bk_cloud_id": 0, "ip": x} for x in eval(hosts)]
    for global_l in global_lists:
        if 'server' in global_l:
            var_server = global_l
            break
    var_server['server'] = {'ip_list': ip_lists}
    # print(var_server)
    date = {
        "bk_biz_id": biz_id,
        "job_plan_id": job_id,
        "global_var_list": [var_server]
    }
    client = get_client_by_request(request)
    result = client.job.execute_job_plan(date)

    # 将请求结果存入数据库
    custom_id = str(uuid.uuid1())

    insert_history = {
        "biz_id": biz_id,
        "tmp_id": job_id,
        "inst_id": result['data']['job_instance_id'],
        "log_id": custom_id,
        "created_time": datetime.datetime.now()
    }
    for ip in eval(hosts):
        insert_log = {
            "ip": ip,
            "content": '',
            "custom_id": custom_id,
        }
        Logs.objects.create(**insert_log)
    History.objects.create(**insert_history)
    log_result.get_logs.delay(request.user.username, biz_id, result['data']['job_instance_id'], custom_id)
    # 调用接口，异步处理任务信息
    return JsonResponse({"data": "", "code": 0, "message": ""})


def get_history_info(request):
    page = request.GET.get('page', 1)
    pagesize = request.GET.get('pagesize', 10)
    all_count = History.objects.count()
    paginator = Paginator(History.objects.order_by("-created_time"), int(pagesize))
    historys = paginator.page(int(page))
    history_lists = [info.to_dict() for info in historys]

    res = all_business(request, d=True)
    biz_dict = {r['bk_biz_id']: r['bk_biz_name'] for r in res}
    for li in history_lists:
        li['biz_id'] = biz_dict[li['biz_id']]
        logs_list_detail = []
        if int(li['inst_status']) == 3:
            # 已完成，获取log
            logs = Logs.objects.filter(custom_id=li['log_id'])
            for log in logs:
                logs_list_detail.append(log.to_dict())
        li['logs'] = logs_list_detail
    data = {
        "data": history_lists,
        "count": all_count,
        "code": 0,
        "message": ""
    }
    # print(data)
    return JsonResponse({"data": data})


def search_history_info(request):
    page = request.GET.get('current', 1)
    pagesize = request.GET.get('pagesize', 10)
    biz_id = request.GET.get('biz_id', '')
    end_time = request.GET.get('end_time')
    start_time = request.GET.get('start_time')
    all_objs = History.objects.all()
    if biz_id:
        all_objs = all_objs.filter(biz_id=biz_id)
    if start_time:
        all_objs = all_objs.filter(created_time__range=[start_time, end_time])

    all_count = all_objs.count()
    paginator = Paginator(all_objs.order_by("-created_time"), int(pagesize))
    historys = paginator.page(int(page))

    history_lists = [info.to_dict() for info in historys]

    res = all_business(request, d=True)
    biz_dict = {r['bk_biz_id']: r['bk_biz_name'] for r in res}
    for li in history_lists:
        li['biz_id'] = biz_dict[li['biz_id']]
        logs_list_detail = []
        if int(li['inst_status']) == 3:
            # 已完成，获取log
            logs = Logs.objects.filter(custom_id=li['log_id'])
            for log in logs:
                logs_list_detail.append(log.to_dict())
        li['logs'] = logs_list_detail
    data = {
        "data": history_lists,
        "count": all_count,
        "code": 0,
        "message": ""
    }
    return JsonResponse({"data": data})


