# -*- coding: utf-8 -*-
import copy
import datetime
import re
from check_system.celery_task.track_task_result import task_celery
from check_system.common.req import req_body_to_json
from check_system.common.request import Request
from check_system.decorator import Log
from check_system.logic.TplLogic import TplLogic
from check_system.models import Tpl, Quota, TaskResult
from check_system.models.models import CheckSystemTplQuta, CheckSystemOs
from check_system.models.task import Task
from check_system.link_tool.redis_client import *
from check_system.common.req import req_body_to_json
from check_system.link_tool.qq_email import Mail
from check_system.link_tool.tool import Make_Recursion_List, Write_Json_File
from check_system.models.task import TaskNotify

# django imports
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q

# bk
from blueking.component.shortcuts import get_client_by_request
from blueking.component.shortcuts import get_client_by_user
from check_system.common.req import req_body_to_json
from check_system.common.request import Request
from check_system.models.execute_log import ExecuteLog
from check_system.apis.ceshi import ceshi_celery

def task_detail(request):
    """
    任务详情
    :param request:
    :return:
    """
    task_id = request.GET.get('task_id')
    if not task_id:
        return Request.errorFcun(msg='参数获取失败')
    result = Task.objects.filter(id=task_id)
    if len(result) > 0:
        return Request.succFcun(data=[a.to_dict_detail() for a in result][0])
    else:
        return Request.errorFcun()


def fetch_task_list(request):
    """
    任务列表
    :param request:
    :return:
    """
    exec_biz_id = request.GET.get('biz_id', "")
    task_os = request.GET.get('os_id', "")
    exec_state = request.GET.get('exec_state', "")
    task_tpl_id = request.GET.get('tpl_id', "")

    # 分页
    # 获取当前页
    page = int(request.GET.get('page', 1))
    # 获取总页数
    size = int(request.GET.get('size', 10))
    # 模糊查询
    keywords = request.GET.get('keywords', '')
    # 日期查询
    date = request.GET.get('date', '')


    old_filed = {
        "is_deleted": 0,
        "exec_biz_id": exec_biz_id,
        "exec_state": exec_state,
        "task_os": task_os,
        "task_name__contains": keywords,
        "task_tpl_id": task_tpl_id,
        "start_time__range": date.split(',') if date != "" else ""
    }
    filed = {}
    for key, value in old_filed.items():
        if value != "":
            filed[key] = value


    result = Task.objects.filter(**filed).order_by('-created_time')

    if result.exists():
        try:
            # 获取前端传来的页码数(需要分几页)
            paginator = Paginator(result, int(size))
            # 获取分好后数据的某一页
            scripts_ = paginator.page(int(page))
        except Exception as err:
            # 没传参则默认分页
            paginator = Paginator(result, 10)
            scripts_ = paginator.page(1)

        # 获取对应的模板数据，OS数据，业务数据
        kwargs = {
            # 'bk_token': 'G6nuRLYKeKF2SKV2toXRNQVL9GWhOetUafkIMcsSSOM',
            "fields": [
                "bk_biz_id",
                "bk_biz_name"
            ],
        }
        client = get_client_by_request(request)
        res = client.cc.search_business(kwargs)
        # 业务模板
        bk_info_lists = {bk['bk_biz_id']: bk['bk_biz_name'] for bk in res['data']['info']}
        # 查询OS模板
        os_info_lists = {os.id: os.to_dict()['os_name'] for os in CheckSystemOs.objects.all()}
        # 查询指标模板
        tpl_info_lists = {tpl.id: tpl.to_dict_name()['tpl_name'] for tpl in Tpl.objects.all()}

        data = [x.to_dict(
            bk_info_lists=bk_info_lists,
            os_info_lists=os_info_lists,
            tpl_info_lists=tpl_info_lists,
        ) for x in scripts_]
        return Request.succFcun(data={
            'data': data,
            'count': paginator.count
        })
    else:
        return Request.errorFcun()


def task_delete(request):
    """
    删除任务
    :param request:
    :return:
    """
    task_id = request.GET.get('task_id')
    if not task_id:
        return Request.errorFcun(msg='参数获取失败')
    result = Task.objects.filter(id=task_id)
    if result.exists():
        with transaction.atomic():
            result.update(is_deleted=1)
            field_names = Log.get_model_field(Task)
            Log.operation_log(request, Task._meta.verbose_name, result.first(), update_fields={},
                              operation_module_name="任务管理", field_names=field_names, method="DELETE")
        return Request.succFcun(msg='删除成功')
    else:
        return Request.errorFcun()


def business_list(request):
    """
    业务列表。需要和用户权限关联
    :param request:
    :return:
    """
    kwargs = {
        "fields": [
            "bk_biz_id",
            "bk_biz_name"
        ],
    }
    client = get_client_by_user(request.user.username)
    result = client.cc.search_business(kwargs)
    if result["result"]:
        return Request.succFcun(data=result["data"]["info"])
    else:
        return Request.errorFcun()

def business_hosts(request):
    """
    业务下topo
    :param request:
    :return:
    """
    bk_biz_id = int(request.GET.get('bk_biz_id', 2))

    if bk_biz_id <= 0:
        return Request.errorFcun()
    kwargs = {
        "bk_biz_id": bk_biz_id,  # 业务ID
    }
    client = get_client_by_request(request)
    result = client.cc.search_biz_inst_topo(kwargs)
    print(result)
    if result['message'] == "success":
        # 调用递归方法
        res = Make_Recursion_List(result['data'][0])
        return Request.succFcun(data=res)
    return Request.errorFcun()


def TopoHost(request):
    """
    节点下的主机
    :param request:
    :return:
    """
    bk_obj_id = request.GET.get('bk_obj_id')
    bk_inst_id = int(request.GET.get('bk_inst_id', 0))
    bk_biz_id = int(request.GET.get('bk_biz_id', 0))
    # 获取对象，筛掉不符合要求的主机
    # (1, centos) (2, ubuntu) (3, windows)

    os_id = int(request.GET.get('os_id', 0))

    client = get_client_by_request(request)
    result = dict()
    if bk_biz_id <= 0 or bk_inst_id <= 0 or bk_obj_id == "":
        return Request.errorFcun(msg='缺少参数')
    if bk_obj_id == "biz":
        result = client.cc.list_biz_hosts({
            "page": {
                "start": 0,
                "limit": 10,
                "sort": "bk_host_id"
            },
            "bk_biz_id": bk_biz_id,
            "fields": [
                "bk_cloud_id",
                'bk_host_innerip',
                "bk_os_name",
                "bk_host_name"
            ],
        })
    else:
        # 获取集群或者模块下的
        result = client.cc.find_host_by_topo({
            "bk_biz_id": bk_biz_id,
            "bk_obj_id": bk_obj_id,
            "bk_inst_id": bk_inst_id,
            "page": {
                "start": 0,
                "limit": 10
            },
            "fields": [
                "bk_cloud_id",
                'bk_host_innerip',
                "bk_os_name",
                "bk_host_name"
            ],
        })
    # print(result['data']['info'])
    res_data = []
    for os in result['data']['info']:
        if os_id == 1:
            os_res = os['bk_os_name'].find("centos")
            if os_res < 0:
                continue
            else:
                res_data.append(os)
        if os_id == 2:
            os_res = os['bk_os_name'].find("ubuntu")
            if os_res < 0:
                continue
            else:
                res_data.append(os)
        if os_id == 3:
            os_res = os['bk_os_name'].find("Windows")
            if os_res < 0:
                continue
            else:
                res_data.append(os)

    if result['result']:
        return Request.succFcun(data=res_data)
    return Request.errorFcun(msg='获取主机失败')


def task_add(request):
    """
    新增任务
    """
    # req = request.POST
    # 获取参数
    req = req_body_to_json(request)
    task_tpl_id = int(req.get("task_tpl_id", -1))  # 模板ID
    ip_list = req.get("exec_hosts", [])  # ip列表
    exec_hosts = str(ip_list)  # [{'bk_host_innerip': "127.0.0.1",....}]
    # 主机系统
    task_os = int(req.get("task_os", 0))
    # 通知人列表
    notify_usernames = req.get("notify_usernames", "")

    # exec_schedule的注释
    # 1. instant 立即执行
    # 2. interval 定期执行 示例: interval,2020-12-31 (表示从什么时候开始)
    # 3. crontab 周期执行 示例: crontab,1 (表示1天执行一次)
    exec_schedule = req.get("exec_schedule", 0)
    exec_start_time = req.get("exec_start_time", "")
    exec_timece = req.get("exec_timec", 0)
    old_task_id = int(req.get('task_id', 0))

    # 数据校验
    if task_tpl_id <= 0 or exec_schedule == "" or int(req.get("biz_id", 0)) <= 0 or exec_start_time == "" or int(
            task_os) <= 0:
        return Request.errorFcun(msg="参数错误")

    # 查询模板
    tpl = Tpl.objects.filter(id=task_tpl_id)
    if not tpl.exists():
        return Request.errorFcun(msg="参数错误，找不到模板ID")
    tpl_obj = tpl.first()

    # # 模板的指标列表
    # tpl_quota_list = eval(tpl_obj.tpl_quotas)

    # 根据模板iD 查询模板关联指标中间表

    tpl_quota_list = CheckSystemTplQuta.objects.filter(tpl_id=tpl_obj.id).all()
    if len(tpl_quota_list) == 0:
        return Request.errorFcun(msg="参数错误，模板指标是空")

    fields = {
        'task_name': req.get("task_name", tpl_obj.tpl_name),
        'task_tpl': tpl_obj,
        'task_op': request.user.username,
        'task_os': task_os,
        'exec_hosts': exec_hosts,
        'exec_biz_id': req.get("biz_id", 0),
        'exec_acc': req.get("exec_acc", "root"),  # 此处写死了root，但后期应该修改为可以配置的 因为系统可能是windows，或者有专门的系统用户执行脚本
        'exec_schedule': exec_schedule,
        'exec_state': 0,
        'exec_progress': 0,
        'exec_quota_total': len(tpl_quota_list),
        'exec_start_time': exec_start_time,
        'exec_timece': exec_timece,
        'start_time': datetime.datetime.now()
    }
    task_obj = {}
    if old_task_id > 0:
        with transaction.atomic():
            old_task_obj = Task.objects.get(pk=old_task_id)
            task_obj = Task.objects.filter(id=old_task_id)
            task_obj.update(**fields)
            old_task_notifys = TaskNotify.objects.filter(task_id=old_task_id).all()
            old_notify_username_list = [old_task_notify.username for old_task_notify in old_task_notifys]
            to_delete_notify_username_list = []
            to_add_notify_username_list = []
            for old_notify_username in old_notify_username_list:
                if old_notify_username not in notify_usernames:
                    to_delete_notify_username_list.append(old_notify_username)
            for new_notify_username in notify_usernames:
                if new_notify_username not in old_notify_username_list:
                    to_add_notify_username_list.append(new_notify_username)
            TaskNotify.objects.filter(Q(task_id=old_task_id) & Q(username__in=to_delete_notify_username_list)).delete()
            to_add_task_notify_list = []
            for username in to_add_notify_username_list:
                new_task_notify = TaskNotify(
                    task_id=old_task_id,
                    username=username
                )
                to_add_task_notify_list.append(new_task_notify)
            TaskNotify.objects.bulk_create(to_add_task_notify_list)

            fields['start_time'] = fields['start_time'].strftime("%Y-%m-%d %H:%M:%S")
            fields['end_time'] = ''
            fields['task_tpl'] = fields['task_tpl'].id
            fields['task_os'] = CheckSystemOs.objects.get(pk=task_os).os_name
            field_names = Log.get_model_field(Task)
            Log.operation_log(request, Task._meta.verbose_name, old_task_obj, update_fields=fields,
                              operation_module_name="任务管理", method="PUT", field_names=field_names)
    else:
        # 校验任务名称是否已经存在
        task_name = Task.objects.filter(task_name=req.get("task_name", ''))

        if len([x for x in task_name]) >= 1:
            return Request.errorFcun(msg="任务名重复")
        with transaction.atomic():
            task = Task.objects.create(**fields)
            task_obj = Task.objects.filter(id=task.id)
            task_notify_list = []
            for username in notify_usernames:
                task_notify = TaskNotify(
                    task_id=task.id,
                    username=username
                )
                task_notify_list.append(task_notify)
            TaskNotify.objects.bulk_create(task_notify_list)
            fields['start_time'] = fields['start_time'].strftime("%Y-%m-%d %H:%M:%S")
            fields['end_time'] = ''
            fields['task_tpl'] = fields['task_tpl'].id
            fields['task_os'] = CheckSystemOs.objects.get(pk=task_os).os_name
            field_names = Log.get_model_field(Task)
            Log.operation_log(request, table_name=Task._meta.verbose_name, update_fields=fields,
                              operation_module_name="任务管理", field_names=field_names)
    return Request.succFcun(data=[info.to_dict_detail() for info in task_obj])


# 任务循环
def execute_task(request):
    """
    执行任务

    按脚本执行
    """
    req = req_body_to_json(request)
    # req = request.GET
    task_id = int(req.get('task_id', 99))

    # 数据校验
    if task_id <= 0:
        return Request.errorFcun(msg='参数错误')

    # 校验数据库是否存在已经执行的任务
    res = redis_link.hget(name="current_task", key=task_id)
    if not res:
        redis_link.hset(name="current_task", key=task_id, value="True")
    else:
        return Request.errorFcun(msg='任务已经在执行中')

    # 查询所在任务数据
    tasks = Task.objects.filter(id=task_id)
    if not tasks.exists():
        return Request.errorFcun(msg='参数错误,找不到这个任务')
    # 获取任务数据行
    task = tasks.first()


    # 查询模板
    tpl = Tpl.objects.filter(id=task.task_tpl_id)
    if not tpl.exists():
        return Request.errorFcun(msg='参数错误,找不到这个模板ID')
    tplLogic = TplLogic()
    tpl_quota_list = tplLogic.getQuotas(task.task_tpl_id)

    if len(tpl_quota_list) == 0:
        return Request.errorFcun(msg='模板的指标是空的，请先添加模板指标')

    # 启动celery任务
    task_celery.delay(task, task.id, request.user)

    field_names = Log.get_model_field(Task)

    Log.operation_log(request, Task._meta.verbose_name, task, update_fields={}, operation_module_name="任务管理",
                      field_names=field_names, method="EXECUTE")
    return Request.succFcun()


def fetch_user_list(request):
    client = get_client_by_request(request)
    req = {
        "no_page": True
    }
    result = client.usermanage.list_users(req)
    data = result.get("data", [])
    if isinstance(data, list):
        return Request.succFcun(data=data)
    else:
        return Request.errorFcun()


def off_button(request):
    task_id = int(request.GET.get('task_id', 181))
    if task_id <= 0:
        return Request.errorFcun(msg='参数获取失败')
    res = redis_link.get(task_id)

    if res != None:
        res_dict = eval(res)
        res_dict['status'] = 'executed'
        redis_link.delete(task_id)
        redis_link.set(task_id, str(res_dict))
        # 改变任务表中的状态
        Task.objects.filter(id=task_id).update(exec_state=0)
    else:
        return Request.errorFcun(msg='获取失败')
    return Request.succFcun(msg='任务停止中')




