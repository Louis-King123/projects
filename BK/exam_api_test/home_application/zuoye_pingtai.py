# !/usr/bin python3                                 
# encoding    : utf-8 -*-                            
# @author     :   shexiaolong                               
# @software   : PyCharm      
# @file       :   zuoye_pingtai.py
# @Time       :   2021/4/21 11:01 上午
import json
import time

from blueking.component.shortcuts import get_client_by_request
from django.http import JsonResponse
from django.conf import settings
from blueking.component.client import ComponentClient


# ###########  作业平台 ##############
class ZuoYePlatform(object):

    @classmethod
    def get_account_list(cls, request):
        """查询业务下的执行账号 查询业务下用户有权限的执行账号列表"""
        biz_id = request.GET.get('biz_id', 2)
        kwargs = {'bk_biz_id': biz_id}
        client = get_client_by_request(request)
        info = client.job.get_account_list(kwargs)
        """
        返回结果所有参数
        category	1        账号用途（1：系统账号，2：DB账号）
        bk_biz_id	2
        account	"root"
        creator	"admin"
        last_modify_time	1616504432218
        alias	"root"
        create_time	1616504432218
        last_modify_user	"admin"
        type	1           账号类型（1：Linux，2：Windows，9：MySQL，10：Oracle，11：DB2）
        id	1
        """
        return JsonResponse({"data": info['data']})

    @classmethod
    def get_cron_list(cls, request):
        """查询业务下定时作业信息"""
        biz_id = request.GET.get('biz_id', 2)
        kwargs = {'bk_biz_id': biz_id}
        client = get_client_by_request(request)
        info = client.job.get_cron_list(kwargs)
        # return JsonResponse(info)
        return JsonResponse({"data": info['data']})

    @classmethod
    def get_cron_detail(cls, request):
        """查询定时作业详情"""
        biz_id = request.GET.get('biz_id', 2)
        corn_id = request.GET.get('corn_id', 9)  # 定时任务ID
        # kwargs = {'bk_biz_id': biz_id}
        kwargs = {'bk_biz_id': biz_id, 'id': corn_id}  # 文档错误， id为必填项
        client = get_client_by_request(request)
        info = client.job.get_cron_detail(kwargs)
        if info['result']:
            data = info['data']
            # global_var_list = data['global_var_list']     # TODO 添加定时任务后，获取详情时没有global_var_list
            # job_plan_id = data['job_plan_id']  # 执行方案ID
            #
            # print(global_var_list)
            return JsonResponse(info)
        else:
            return JsonResponse({'data': '', 'status': False})
        # return JsonResponse({"data": info['data']})

    @classmethod
    def get_job_plan_list(cls, request):
        """查询执行方案列表"""
        biz_id = request.GET.get('biz_id', 2)
        kwargs = {
            'bk_biz_id': biz_id,
        }
        client = get_client_by_request(request)
        info = client.job.get_job_plan_list(kwargs)
        if info['result']:
            return JsonResponse(info)
        else:
            return JsonResponse({'data': '', 'status': False})

    @classmethod
    def get_job_plan_detail(cls, request, job_plan_id=None):
        """根据作业执行方案 ID 查询作业执行方案详情"""
        biz_id = request.GET.get('biz_id', 2)
        if not job_plan_id:
            job_plan_id = request.GET.get('job_plan_id', 2)  # 要定时执行的作业的执行方案 ID
        kwargs = {
            'bk_biz_id': biz_id,
            'job_plan_id': job_plan_id
        }
        client = get_client_by_request(request)
        info = client.job.get_job_plan_detail(kwargs)
        if info['result']:
            return JsonResponse({'data': info['data']})
        else:
            return JsonResponse({'data': '', 'status': False})

    @classmethod
    def save_cron(cls, request):  # TODO 添加定时任务后，获取详情时没有global_var_list
        """新建或保存定时作业；新建定时作业，定时任务状态默认为暂停"""
        biz_id = request.GET.get('biz_id', 2)
        job_plan_id = request.GET.get('job_plan_id', 2)  # 要定时执行的作业的执行方案 ID
        plan_detail = cls.get_job_plan_detail(request, job_plan_id=job_plan_id)
        global_var_list = json.loads(plan_detail.content)['data']['global_var_list']
        kwargs = {
            'bk_biz_id': biz_id,
            'job_plan_id': job_plan_id,
            "expression": "* */1 * * *",
            'name': 'she-test-corn-2',
            'global_var_list': global_var_list
        }

        client = get_client_by_request(request)
        info = client.job.save_cron(kwargs)
        return JsonResponse(info)

    @classmethod
    def save_cron_update(cls, request):  # TODO 添加定时任务后，获取详情时没有global_var_list
        """新建或保存定时作业；新建定时作业，定时任务状态默认为暂停"""
        biz_id = request.GET.get('biz_id', 2)
        job_plan_id = request.GET.get('job_plan_id', 2)  # 要定时执行的作业的执行方案 ID
        corn_id = request.GET.get('corn_id', 9)  # 定时任务 ID
        plan_detail = cls.get_job_plan_detail(request, job_plan_id=job_plan_id)
        global_var_list = json.loads(plan_detail.content)['data']['global_var_list']
        kwargs = {
            'bk_biz_id': biz_id,
            'id': corn_id,
            'job_plan_id': job_plan_id,
            "expression": "* */1 * * *",
            'name': 'she-test-corn-update',
            'global_var_list': global_var_list
        }

        client = get_client_by_request(request)
        info = client.job.save_cron(kwargs)
        return JsonResponse(info)

    @classmethod
    def update_cron_status(cls, request):
        """更新定时作业状态，如启动或暂停
        省略获取定时任务  get_cron_list
        """
        biz_id = request.GET.get('biz_id', 2)
        corn_id = request.GET.get('corn_id', 10)  # 定时任务 ID
        kwargs = {
            'bk_biz_id': biz_id,
            'id': corn_id,  # 定时作业 ID
            # 'status': 1  # 定时状态，1.启动、0.暂停     文档错误 文档中2是暂停
            'status': 0  # 定时状态，1.启动、0.暂停
        }
        client = get_client_by_request(request)
        info = client.job.update_cron_status(kwargs)
        if info['result']:
            return JsonResponse({'data': info['data']})
        else:
            return JsonResponse(info)

    # ***********
    @classmethod
    def execute_job_plan(cls, request):
        """执行作业执行方案   启动作业执行方案"""
        biz_id = request.GET.get('biz_id', 2)
        job_plan_id = request.GET.get('job_plan_id', 2)  # 作业执行方案ID
        plan_detail = cls.get_job_plan_detail(request, job_plan_id=job_plan_id)
        global_var_list = json.loads(plan_detail.content)['data']['global_var_list']
        kwargs = {
            'bk_biz_id': biz_id,
            'job_plan_id': job_plan_id,  # 定时作业 ID
            'global_var_list': global_var_list,
        }
        client = get_client_by_request(request)
        info = client.job.execute_job_plan(kwargs)
        if info['result']:
            return JsonResponse(info)
        else:
            return JsonResponse(info)
        # return JsonResponse(kwargs)

    @classmethod
    def get_job_instance_status(cls, request):
        """根据作业实例 ID 查询作业执行状态"""
        biz_id = request.GET.get('biz_id', 2)
        # job_instance_id是执行execute_job_plan后获取到的 这里省略获取逻辑
        job_instance_id = request.GET.get('job_instance_id', 20000000301)  # 作业实例ID
        kwargs = {
            'bk_biz_id': biz_id,
            'job_instance_id': job_instance_id,  # 作业实例ID
        }
        client = get_client_by_request(request)
        info = client.job.get_job_instance_status(kwargs)
        if info['result']:
            return JsonResponse(info)
        else:
            return JsonResponse(info)

    @classmethod
    def get_job_instance_ip_log(cls, request):
        """根据作业实例 ID 查询作业执行日志 根据ip查询作业执行日志"""
        biz_id = request.GET.get('biz_id', 2)
        # 所有需要的参数目前都是默认的，后续会整理  step_instance_id 通过get_job_instance_status 获取
        job_instance_id = request.GET.get('job_instance_id', 20000000294)  # 作业实例ID
        ip_list = ['172.27.1.63', '172.27.0.96']
        step_instance_id = ['20000000295', '20000000296']
        client = get_client_by_request(request)
        for ip in ip_list:
            for step in step_instance_id:
                print(ip, '----------', step)
                kwargs = {
                    'bk_biz_id': biz_id,
                    'job_instance_id': job_instance_id,  # 作业实例ID
                    'step_instance_id': int(step),  # 步骤实例ID
                    'bk_cloud_id': 0,
                    'ip': ip
                }

                info = client.job.get_job_instance_ip_log(kwargs)
                print(info['data']['log_content'])
        # if info['result']:
        #     return JsonResponse(info)
        # else:
        #     return JsonResponse(info)
        return JsonResponse({'data': 'success'})


#  执行执行计划并获取执行结果
class DoJobPlan(object):

    @classmethod
    def execute_job_and_get_log(cls, request):
        """业务ID和job_plan_id是事先给到的
        流程：业务--主机--选取主机--获取job详情--拼接参数--执行job--获取job执行结果--根据执行job的job_instance_id获取步骤step_id--循环主机和步骤获取每一个步骤的执行结果
        """
        bk_biz_id = 2
        job_plan_id = 2
        host_ip_list = []
        step_instance_list = []

        # 获取业务
        business = cls.search_business(request)

        # 根据业务获取主机列表
        hosts = cls.list_biz_hosts(request, bk_biz_id)

        # 选择3个主机   测试模拟页面选择的机器 默认为3个
        for host in hosts[0:3]:
            host_ip_list.append(host['bk_host_innerip'])

        # 拼接global_var_list 中的ip_list参数
        ip_list = [{'bk_cloud_id': 0, 'ip': ip} for ip in host_ip_list]

        # 获取job详情 获取 global_var_list
        job_plan_detail = cls.get_job_plan_detail(request, bk_biz_id, job_plan_id)
        # 将ip_list放到global_var_list中
        global_var_list = job_plan_detail['global_var_list']
        for var in global_var_list:
            if 'server' in var:
                var['server']['ip_list'] = ip_list

        # 执行job_plan
        job_plan_result = cls.execute_job_plan(request, bk_biz_id, job_plan_id, global_var_list)
        job_instance_id = job_plan_result['job_instance_id']
        # job_instance_id = 20000000301

        # 根据job_instance_id 获取执行结果
        job_instance_status_result = cls.get_job_instance_status(request, bk_biz_id, job_instance_id)
        if job_instance_status_result:
            # 获取step_id
            step_list = job_instance_status_result['step_instance_list']
            for step in step_list:
                step_instance_list.append(step['step_instance_id'])

            # 根据ip， step_id获取执行结果
            log_content_result = \
                cls.get_job_instance_ip_log(request, bk_biz_id, job_instance_id, host_ip_list, step_instance_list)
            return JsonResponse({'data': log_content_result})
        else:
            return JsonResponse({'data': '执行失败'})

    @classmethod
    def search_business(cls, request):
        """
        查询业务
        result: 2/蓝鲸，5/自动巡检 ......
        """
        client = get_client_by_request(request)
        kwargs = {
            "fields": [
                "bk_biz_id",
                "bk_biz_name"
            ],
            "page": {
                "start": 0,
                "limit": 100,
                "sort": ""
            }
        }

        info = client.cc.search_business(kwargs)

        return info['data']['info']

    @classmethod
    def list_biz_hosts(cls, request, bk_biz_id):
        """查询业务下的主机
        根据业务 ID 查询业务下的主机，可附带其他的过滤信息，如集群 id 多个用逗号隔开,模块 id 多个用逗号隔开
        """
        client = get_client_by_request(request)

        kwargs = {"page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_id"
        },
            "fields": [
                "bk_host_id",
                "bk_cloud_id",
                "bk_host_innerip",
                "bk_os_type",
                "bk_mac"
            ],
            'bk_biz_id': bk_biz_id}

        info = client.cc.list_biz_hosts(kwargs)
        return info['data']['info']

    @classmethod
    def get_job_plan_detail(cls, request, biz_id, job_plan_id):
        """根据作业执行方案 ID 查询作业执行方案详情"""
        kwargs = {
            'bk_biz_id': biz_id,
            'job_plan_id': job_plan_id
        }
        client = get_client_by_request(request)
        info = client.job.get_job_plan_detail(kwargs)
        return info['data']

    @classmethod
    def execute_job_plan(cls, request, biz_id, job_plan_id, global_var_list):
        """执行作业执行方案   启动作业执行方案"""
        kwargs = {
            'bk_biz_id': biz_id,
            'job_plan_id': job_plan_id,  # 定时作业 ID
            'global_var_list': global_var_list,
        }
        client = get_client_by_request(request)
        info = client.job.execute_job_plan(kwargs)
        return info['data']

    @classmethod
    def get_job_instance_status(cls, request, biz_id, job_instance_id):
        """根据作业实例 ID 查询作业执行状态"""
        kwargs = {
            'bk_biz_id': biz_id,
            'job_instance_id': job_instance_id,  # 作业实例ID
        }
        client = get_client_by_request(request)
        info = client.job.get_job_instance_status(kwargs)
        retry = 5
        data = None
        while retry:
            if info['result'] and info['data']['finished'] and info['data']['job_instance']['status'] == 3:
                retry = 0
                data = info['data']
            else:
                retry -= 1
                time.sleep(5)

        return data

    @classmethod
    def get_job_instance_ip_log(cls, request, biz_id, job_instance_id, ip_list, step_instance_id):
        """根据作业实例 ID 查询作业执行日志 根据ip查询作业执行日志"""
        client = get_client_by_request(request)
        log_content = []
        for ip in ip_list:
            for step in step_instance_id:
                kwargs = {
                    'bk_biz_id': biz_id,
                    'job_instance_id': job_instance_id,  # 作业实例ID
                    'step_instance_id': int(step),  # 步骤实例ID
                    'bk_cloud_id': 0,
                    'ip': ip
                }

                info = client.job.get_job_instance_ip_log(kwargs)
                log_content.append({'ip': ip, 'log_content': info['data']['log_content']})

        return log_content
