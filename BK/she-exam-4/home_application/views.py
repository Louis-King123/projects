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
import base64
import time

from django.shortcuts import render
from django.http import JsonResponse
import datetime
from home_application.models import BackupHistory
from blueking.component.shortcuts import get_client_by_request
from config.__init__ import APP_CODE, SECRET_KEY, BK_URL


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
    # return render(request, 'home_application/test.html')


def history(request):
    """
    首页
    """

    return render(request, 'home_application/history.html')


def api_test(request):
    """
    测试接口
    """
    return JsonResponse({"message": "hello world",
                         "data":
                             {"user": request.user.username,
                              "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                         "result": "true"})


def get_secret(request):
    """
    获取BK token
    """
    bk_token = request.COOKIES.get('bk_token')
    return bk_token


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


def search_topo(request):
    """
    查询拓扑
    """

    result_topo = [
                    {
                        'name': '集群[批量启动进程模块1]',
                        'expanded': 'true',
                        id: 1,
                        'children': [
                            {'name': 'testwa.fda.1.1', id: 2},
                            {'name': 'testwa.fda.1.2', id: 3},
                            {'name': 'testwa.fda.1.3', id: 4, 'parentId': 1},
                            {
                                'name': '集群[批量启动进程子模块1]',
                                'expanded': 'true',
                                id: 5,
                                'children': [
                                    {'name': 'testwa.fda.2.1', id: 6},
                                    {'name': 'testwa.fda.2.2', id: 7},
                                    {'name': 'testwa.fda.2.3', id: 8}
                                ]
                            },
                            {'name': '集群[批量启动进程子模块2]', id: 9},
                            {'name': '集群[批量启动进程子模块3]', id: 10},
                            {'name': '集群[批量启动进程子模块4]', id: 11}
                        ]
                    }
                ]
    result_topo_list = []
    biz_id = request.GET.get('biz_id', '')
    client = get_client_by_request(request)
    kwargs = {'bk_biz_id': biz_id}
    result = client.cc.search_biz_inst_topo(kwargs)
    for topo in result['data']:
        biz_dict = {
            'name': topo['bk_inst_name'],
            'expanded': True,
            'bk_obj_id': 'biz',
            'id': biz_id
        }
        print(biz_dict)
        set_child = []
        for op in topo['child']:
            if len(op['child']):
                model_child = []
                for mo in op['child']:
                    model_child.append({'name': mo['bk_inst_name'], 'id': mo['bk_inst_id'], 'bk_obj_id': mo['bk_obj_id']})
                set_child.append({'name': op['bk_inst_name'], 'id': op['bk_inst_id'], 'expanded': False,
                                  'children': model_child, 'bk_obj_id': op['bk_obj_id']})
            else:
                set_child.append({'name': op['bk_inst_name'], 'id': op['bk_inst_id'], 'bk_obj_id': op['bk_obj_id']})
        biz_dict['children'] = set_child
        result_topo_list.append(biz_dict)
    return JsonResponse({"data": result_topo_list})
    # return JsonResponse({"data": result})


def list_topo_hosts(request):
    """
    查询拓扑节点下的主机
    """

    bk_biz_id = request.GET.get('bk_biz_id', '')
    bk_obj_id = request.GET.get('bk_obj_id', '')
    bk_inst_id = request.GET.get('bk_inst_id', '')
    client = get_client_by_request(request)
    kwargs = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_token": get_secret(request),
        "bk_biz_id": int(bk_biz_id),
        "bk_obj_id": bk_obj_id,
        "bk_inst_id": int(bk_inst_id),
        "fields": [
            "bk_cloud_id",
            "bk_host_innerip"
        ],
        "page": {
            "start": 0,
            "limit": 500
        }
    }
    result = client.cc.find_host_by_topo(kwargs)
    # 解析获取主机ip
    ip_list = []
    try:
        for ip_info in result['data']['info']:
            ip_list.append(ip_info['bk_host_innerip'])
            print(ip_info['bk_host_innerip'])
    except:
        pass
    # return JsonResponse({"data": result})
    return JsonResponse({"data": ','.join(ip_list)})


def list_biz_hosts(request):
    """
    查询业务下的主机
    """
    bk_biz_id = request.GET.get('bk_biz_id', '')
    bk_obj_id = request.GET.get('bk_obj_id', '')
    bk_inst_id = request.GET.get('bk_inst_id', '')
    client = get_client_by_request(request)
    kwargs = {
        "page": {
            "start": 0,
            "limit": 500,
            "sort": "bk_host_id"
        },
        "bk_biz_id": bk_biz_id,
        "fields": [
            "bk_host_id",
            "bk_cloud_id",
            "bk_host_innerip",
            "bk_os_type",
            "bk_mac"
        ],
        f"bk_{bk_obj_id}_ids": [int(bk_inst_id)],
    }
    print(bk_obj_id)
    result = client.cc.list_biz_hosts(kwargs)

    return JsonResponse({"data": result})


def job_detail(request):
    """
    job详情
    """
    biz_id = request.GET.get('biz_id', '')
    job_id = request.GET.get('job_id', '')
    date = {
        "bk_biz_id": biz_id,
        "job_plan_id": job_id
    }
    client = get_client_by_request(request)
    result = client.job.get_job_plan_detail(date)
    return result


def get_biz_account_users(request):
    """
    查询业务下用户有权限的执行账号列表
    """
    kwargs = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_token": get_secret(request),
        "bk_biz_id": int(request.GET.get('bk_biz_id')),
        "category": 1,
        "start": 0,
        "length": 100
    }

    client = get_client_by_request(request)
    result = client.usermanage.get_account_list(kwargs)
    for data in result['data']:
        if int(data['category']) == 1 and int(data['type']) == 1:
            return int(data['id'])
    return 0


def fast_exce_script(request):
    """
    快速执行脚本，统计指定机器，指定目录，指定后缀的文件
    """
    ips = request.GET.get('ips', '')
    direct = request.GET.get('direct', '')
    file_name = request.GET.get('file_name', '')
    bk_biz_id = request.GET.get('bk_biz_id', '')
    script = """
    cd %s || return
    find . -name "*.%s" -maxdepth 1| sed "s;./;;g"| xargs du -ck
    """ % (direct, file_name)
    # 脚本内容base64
    script_content = str(base64.b64encode(script.encode("utf8")), "utf8")
    # 查询业务下用户有权限的执行账号列表
    account_id = get_biz_account_users(request)
    # 组装IP
    ip_lists = [{"bk_cloud_id": 0, "ip": x} for x in ips.split(',')]

    kwargs = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_token": get_secret(request),
        "bk_biz_id": int(bk_biz_id),
        "timeout": 1000,
        "script_language": 1,
        "script_content": script_content,
        "account_id": account_id,
        "target_server": {'ip_list': ip_lists},
        "page": {
            "start": 0,
            "limit": 500
        }
    }

    client = get_client_by_request(request)
    result = client.job.fast_execute_script(kwargs)
    # 获取日志
    exec_script_result = alay_fast_script_result(request, result, ips.split(','))
    # 解析日志
    all_data = []
    for sr in exec_script_result:
        sc_log_content = sr['log_content'].split('\n')
        sc_log_content_split = list(filter(None, sc_log_content))
        file_list = [i.split('\t')[-1] for i in sc_log_content_split[0:-1]]  # 文件列表
        total_size = sc_log_content_split[-1].split('\t')[0]
        all_data.append({
            'ip': sr['ip'],
            'file': ','.join(file_list),
            'size': total_size,
            'count': len(file_list),
        })
    return JsonResponse({"data": all_data})
    # return JsonResponse({"data": exec_script_result})


def alay_fast_script_result(request, result, ips):
    """
    解析快速执行脚本内容
    现获取状态，在获取日志，然后解析日志
    """
    job_instance_id = result['data']['job_instance_id']
    bk_biz_id = request.GET.get('bk_biz_id', '')
    date = {"bk_biz_id": bk_biz_id, "job_instance_id": job_instance_id}

    client = get_client_by_request(request)
    for i in range(0, 13):
        status_result = client.job.get_job_instance_status(date)
        if status_result['data']['job_instance']['status'] == 3:
            step_instance_list = []
            log_result_list = []
            # print(status_result)
            # 获取所有step_instance_id
            instance_list = status_result['data']['step_instance_list']
            for step in instance_list:
                step_instance_list.append(step['step_instance_id'])
                # print('------')
                # print(step_instance_list)
            for step_id in step_instance_list:
                for ip in ips:
                    ip_log_data = {
                        'bk_biz_id': bk_biz_id,
                        'job_instance_id': job_instance_id,
                        'step_instance_id': int(step_id),
                        'bk_cloud_id': 0,
                        'ip': ip,
                    }
                    log_result = client.job.get_job_instance_ip_log(ip_log_data)
                    log_result_list.append(log_result['data'])
            return log_result_list
        else:
            time.sleep(5)
    else:
        return []


# ==========执行job===============
def job_list(request):
    """
    作业模版详情
    """
    biz_id = request.GET.get('bk_biz_id', '')
    client = get_client_by_request(request)
    date = {
        "bk_biz_id": biz_id,
    }
    result = client.job.get_job_plan_list(date)
    return JsonResponse({"data": result['data']})


def job_detail(request):
    """
    job详情
    默认job_id=1000006 （自己创建的）
    """
    bk_biz_id = request.GET.get('bk_biz_id', '')
    # job_id = request.GET.get('job_id', '')
    date = {
        "bk_biz_id": bk_biz_id,
        "job_plan_id": 1000006
    }
    client = get_client_by_request(request)
    result = client.job.get_job_plan_detail(date)
    return result


def execute_backup(request):
    """
    执行备份
    """

    ip = request.GET.get('ip', '')
    direct = request.GET.get('direct', '')
    file_name = request.GET.get('file_name', '')
    file = request.GET.get('file', '')
    bk_biz_id = request.GET.get('bk_biz_id', '')
    count = request.GET.get('count', '')
    size = request.GET.get('size', '')

    job_detail_result = job_detail(request)
    backup_name = 'backup' + str(int(time.time())) + '.tar'
    global_var_list = job_detail_result['data']['global_var_list']
    for var in global_var_list:
        if var['name'] == "direct":
            var['value'] = direct
        elif var['name'] == "fileSerfix":
            var['value'] = file_name
        elif var['name'] == "backupName":
            var['value'] = backup_name
        if var['name'] == "IP":
            var['server']['ip_list'] = [{'ip': ip, 'bk_cloud_id': 0}]
    # 自己测试，需要传入值，考试时只需要更改IP
    date = {
        "bk_biz_id": int(bk_biz_id),
        "job_plan_id": 1000006,
        "global_var_list": global_var_list
    }
    client = get_client_by_request(request)
    result = client.job.execute_job_plan(date)

    # 如果结果中的result = true，则把数据存入数据库
    if result['result']:
        job_url = BK_URL.replace('paas', 'job')
        job_url_final = job_url + '/' + str(bk_biz_id) + '/execute/task/' + str(result['data']['job_instance_id'])
        kw_result = {
            'ip': ip,
            'file_list': file,
            'file_count': count,
            'file_size': size,
            'backup_person': request.user.username,
            'job_link': job_url_final
        }
        BackupHistory.objects.create(**kw_result)
        return JsonResponse({"data": result, "code": 0})
    else:
        return JsonResponse({"data": "", "code": 1})


# ###########################备份历史#####################################

def history_info(request):
    historys = BackupHistory.objects.all().order_by('-backup_time')
    all_data = [h.to_dict() for h in historys]
    return JsonResponse({"data": all_data})





