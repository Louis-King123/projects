# -*- coding: utf-8 -*-
"""
巡检报告API
"""
import datetime
import json
from operator import itemgetter
from itertools import groupby

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.views.generic.base import View

from check_system.common.request import Request
from check_system.common.get_client import get_biz_os_tpl
from check_system.common import utils
from check_system.models import CheckSystemClass
from check_system.models.task import Task
from check_system.models.task_result import TaskHostResult
from check_system.models.models import CheckSystemOs
from check_system.models.tpl import Tpl
from check_system.common.req import req_body_to_json
from check_system.models.execute_log import ExecuteLog
from check_system.models.quota import Quota
from check_system.util_log import logger


class InspectionReport(View):

    @classmethod
    def get(cls, request, *args, **kwargs):
        """
        根据历史报告的ID获取巡检报告的详情
        如果存在report_id,则获取指定ID的巡检报告
        不存在ID，则获取最新的巡检报告
        """
        # 定义字典，存放业务，后续报告中根据biz_id获取业务名称
        biz_dict = dict()
        execute_id = request.GET.get("id", '')

        # 获取所有业务
        dates = utils.get_all_biz(request)

        # 过滤业务数据，拼装成json
        business_infos = dates.get('data').get('info')
        for info in business_infos:
            biz_dict[info.get('bk_biz_id')] = info.get('bk_biz_name')

        # 获取执行历史记录，根据execute中的task_id获取task， 如果没有指明id，则获取最新时间的log
        if execute_id:
            execute_result = ExecuteLog.objects.get(pk=execute_id)

        else:
            execute_result = ExecuteLog.objects.filter(exec_state__in=[2, 3]).order_by("-end_time")
            if execute_result:
                execute_result = execute_result.first()
                execute_id = execute_result.id

        # 巡检报告历史不存在
        if not execute_result:
            return Request.errorFcun("巡检报告历史不存在")
        task_result = Task.objects.get(pk=execute_result.task_id)
        task_tpl_name = task_result.task_tpl.tpl_name
        result_dict = task_result.to_dict_detail()  # 对象转json

        result_dict['task_os'] = task_result.task_tpl.get_os_name()
        # 业务名称
        result_dict['bk_biz_name'] = biz_dict.get(task_result.exec_biz_id)

        # 匹配主机结果简报规则
        # 1，从历史主机报告中获取对应执行报告ID的信息
        # 2, 去重获取所有host
        # 3，过滤历史报告执行结果为false， 并获取IP，在去重  异常主机
        # 4，过滤历史报告执行结果为false， 异常指标数
        # 5，在host去重的基础上，判断是否有powerOff, 巡检失败主机数
        result_dict['hosts'] = []

        task_host_results = TaskHostResult.objects.filter(execute_log_id=execute_id)
        all_ips = task_host_results.values_list('host_ip', flat=True).distinct()  # ip去重
        # 巡检主机数
        result_dict['all_ips'] = len(all_ips)
        all_error_hosts = task_host_results.filter(check_result__icontains='powerOff/')
        # all_error_hosts = task_host_results.filter(check_result='powerOff')
        result_dict['failed_host'] = len(all_error_hosts)  # 巡检失败主机数
        # 巡检失败主机IP
        error_host_list = all_error_hosts.values_list('host_ip', flat=True)

        # 异常指标
        error_quotas = task_host_results.exclude(check_result__icontains='powerOff/').filter(result_status=False)
        # error_quotas = task_host_results.exclude(check_result='powerOff').filter(result_status=False)
        result_dict['error_num'] = len(error_quotas)  # 异常指标数
        # 异常主机数
        error_hosts = error_quotas.values_list('host_ip', flat=True).distinct()

        result_dict['error_host'] = len(error_hosts)

        # 将记录和每个主机拼装
        for host in all_ips:
            # 收集主机异常指标
            host_quota = []
            single_host_quotas = error_quotas.filter(host_ip=host)
            for single_host_quota in single_host_quotas:
                host_quota.append({
                    'quota_name': single_host_quota.quota_id.quota_name,
                    'recommend_value': single_host_quota.recommend_value,
                    'check_result': single_host_quota.check_result
                })
            failed_info = ''
            if host in error_host_list:
                error_info = all_error_hosts.filter(host_ip=host).first()
                failed_info = error_info.check_result.split('/')[-1]
            result_dict['hosts'].append({
                'host': host,
                'host_status': 'failed' if host in error_host_list else 'success',
                'bk_biz_name': result_dict['bk_biz_name'],
                'task_name': result_dict['task_name'],
                'task_os': result_dict['task_os'],
                'task_tpl': result_dict['task_tpl'],
                'task_tpl_name': task_tpl_name,
                'errors': host_quota,  # 这里的error是对应机器的异常的列表  #
                'failed_info': failed_info
            })

        execute_dict = execute_result.to_dict()
        result_dict['start_time'] = execute_dict['updated_time']
        result_dict['end_time'] = execute_dict['end_time']
        result_dict['execute_log_id'] = execute_dict['id']
        return Request.succFcun(data=result_dict)

    @classmethod
    def post(cls, request, *args, **kwargs):

        pass


class HistoryReport(View):

    @classmethod
    def get(cls, request, *args, **kwargs):
        """
            获取历史报告列表
            1,获取所有task历史
            2,获取业务，巡检对象，模版
        """
        # 获取参数
        current = request.GET.get("current", 1)
        limit = request.GET.get("limit", 10)
        data_list = list()
        biz_dict = dict()

        # 获取所有业务
        dates = utils.get_all_biz(request)
        # 过滤业务数据，拼装成json
        business_infos = dates.get('data').get('info')
        for info in business_infos:
            biz_dict[info.get('bk_biz_id')] = info.get('bk_biz_name')

        task_kwargs = {
            'task_tpl': request.GET.get("task_tpl", ""),
            'task_os': request.GET.get("task_os", ""),
            'exec_biz_id': request.GET.get("exec_biz_id", "")
        }
        # 删除任务参数空值项
        for task_key in list(task_kwargs.keys()):
            if not task_kwargs[task_key]:
                task_kwargs.pop(task_key)
        # 查询符合条件的任务id
        if task_kwargs:
            task_ids = Task.objects.filter(**task_kwargs).values_list('id', flat=True)
        else:
            task_ids = Task.objects.values_list('id', flat=True)

        execute_kwargs = {
            "exec_state__in": [2, 3],
            "task_id__in": list(task_ids)
        }
        start_time = request.GET.get("start_time", '')
        end_time = request.GET.get("end_time", '')
        if start_time and end_time:
            execute_kwargs["updated_time__gte"] = start_time + " 00:00:00"
            execute_kwargs["end_time__lt"] = end_time + " 23:59:59"
        # 查询执行日志
        execute_logs_queryset = ExecuteLog.objects.filter(**execute_kwargs)
        # 分页数据
        paginator = Paginator(execute_logs_queryset.order_by("-created_time"), int(limit))
        execute_logs = paginator.page(int(current))

        # 以{id：object}形式存储task
        tasks = Task.objects.filter(id__in=[execute.task_id for execute in execute_logs])
        tasks = {task.id: task for task in tasks}

        # 业务模板 查询OS模板 查询指标模板
        bk_info_lists, os_info_lists, tpl_info_lists = get_biz_os_tpl(request)
        dict_kwargs = {
            "bk_info_lists": bk_info_lists,
            "os_info_lists": os_info_lists,
            "tpl_info_lists": tpl_info_lists
        }

        # 获取历史报告
        for execute in execute_logs:
            result = tasks[execute.task_id]
            result_dict = result.to_dict(**dict_kwargs)
            result_dict['bk_biz_name'] = biz_dict.get(result.exec_biz_id)
            result_dict['task_os'] = result.task_tpl.get_os_name()
            result_dict['tpl_name'] = result.task_tpl.tpl_name
            execute_dict = execute.to_dict()
            result_dict['start_time'] = execute_dict['updated_time']
            result_dict['end_time'] = execute_dict['end_time']
            result_dict['execute_log_id'] = execute_dict['id']
            data_list.append(result_dict)
        return Request.succFcun(data={"count": paginator.count, "data": data_list})

class InspectionReportDetail(View):

    @classmethod
    def post(cls, request, *args, **kwargs):
        """
        获取机器运行详情
        参数：os 操作系统，task_id 任务ID  host 操作主机IP
        逻辑：1，根据系统调用不同的方法（不同系统获取参数有差异）
             2，获取对应任务的任务结果
             3，在任务结果中获取对应的机器信息
        """
        try:
            req = req_body_to_json(request)
        except:
            req = {'os': request.POST.get('os'),
                   'execute_id': request.POST.get('execute_id'),
                   'host': request.POST.get('host')}

        # if req.get('os') == 'linux':
        #     return linux_host_detail(req)
        #     # return detail(req)
        # # if req.get('os') == 'centos':
        # #     return linux_host_detail(req, 1)
        # # elif req.get('os') == 'ubuntu':
        # #     return linux_host_detail(req, 2)
        # else:
        #     return windows_host_detail(req)

        fun = {
            'linux': linux_host_detail,
            'windows': windows_host_detail
        }
        return fun[req.get('os')](req)


def detail(req):
    # 根据execute_id获取任务执行历史
    host = req.get('host')
    execute_id = req.get('execute_id')

    # 返回结果
    data = {}

    # 查询是否有此次日志
    execute_obj = ExecuteLog.objects.filter(pk=execute_id).first()  # 任务历史对象

    if not execute_obj:
        return Request.errorFcun('巡检报告详情不存在')

    execute_dict = execute_obj.to_dict()  # 任务历史json对象
    task_host = {
        'host': host,  # 巡检主机
        'create_time': execute_dict.get('created_time'),  # 开始时间
        'end_time': execute_dict.get('end_time')  # 结束时间
    }
    data['task_host'] = task_host

    # 查询本次详情
    host_results = TaskHostResult.objects.filter(host_ip=host, execute_log_id=execute_id)

    quota_total = host_results.count()  # 指标总数
    quota_total_error = host_results.filter(result_status=False).count()  # 异常指数
    quota_list = host_results.values("system_class_id").annotate(c=Count("system_class_id"))  # 根据class分组
    # print(quota_list)
    # print(host_results.values("system_class_id"))

    system_class_ids = []  # class分类id
    for val in quota_list:
        system_class_ids.append(val['system_class_id'])

    # 查询class分类
    system_class = CheckSystemClass.objects.filter(id__in=system_class_ids)
    class_name_map = {}
    for class_val in system_class:
        class_name_map[class_val.id] = class_val.class_name

    top_list = {}  # 面板参数
    for val in quota_list:
        temp_classname = class_name_map[val['system_class_id']]
        top_list[temp_classname] = val['c']
    # print(top_list)
    data_list = {}  # 参数列表页面
    for val in host_results:
        temp = {
            "check_result": val.check_result
        }

        temp_classname = class_name_map.get(val.system_class_id, False)
        if not temp_classname:
            continue

        if temp_classname not in data_list:
            data_list[temp_classname] = []

        data_list[temp_classname].append(temp)

    data = {
        'quota_total': quota_total,
        'quota_total_error': quota_total_error,
        'top_list': top_list,
        'data_list': data_list,
        'task_host': task_host
    }

    # print(data.keys())

    return Request.succFcun(data=data)


def linux_host_detail(req):
    # 根据execute_id获取任务执行历史
    host = req.get('host')
    execute_id = req.get('execute_id')
    try:
        execute_obj = ExecuteLog.objects.get(pk=execute_id)  # 任务历史对象
    except:
        return Request.errorFcun('巡检报告详情不存在')

    execute_dict = execute_obj.to_dict()  # 任务历史json对象
    task_host = {
        'host': host,  # 巡检主机
        'create_time': execute_dict.get('created_time'),  # 开始时间
        'end_time': execute_dict.get('end_time')  # 结束时间
    }

    # 巡检概览
    host_results = TaskHostResult.objects.filter(host_ip=host, execute_log_id=execute_id)
    host_result_errors = host_results.filter(result_status=False)

    # 安全配置信息 [账号安全 class_id=4, 系统安全 class_id=7, SSH安全设置 class_id=8, 用户安全 class_id=9, 网络安全 class_id=11]
    # 判断每一种安全配置是否存在，存在则获取数据，不存在则忽略
    # 安全配置信息里面包含（账号安全，系统安全，SSH安全设置，用户安全，网络安全）
    # 逻辑说明，在巡检结果中先获取对应class id的巡检结果，循环放入列表中，然后将错误信息放入统计的列表
    safe_config_error, system_run_status_error, system_performance_error, system_info_error, account_config, \
    system_safe, ssh_safe, user_safe, inter_safe, system_run_status, system_performance, system_performance_info, \
    system_config_info, base_info, custom_info_data_error, custom_info = analysis_configure_info(host_results)

    try:
        error_percent = float(format(float(host_result_errors.count()) / float(host_results.count()), '.2f')) * 100
    except:
        error_percent = 0
    inspection_info_detail = [
        # 系统检查类型  # 异常个数  # 异常信息
        {'class_name': '安全配置信息', 'error_count': len(safe_config_error),
         'error_info': safe_config_error, 'tag': 'safe_config'},
        {'class_name': '系统运行状态信息', 'error_count': len(system_run_status_error),
         'error_info': system_run_status_error, 'tag': 'system_run_status'},
        {'class_name': '系统性能信息', 'error_count': len(system_performance_error),
         'error_info': system_performance_error, 'tag': 'system_performance'},
        {'class_name': '系统信息', 'error_count': len(system_info_error),
         'error_info': system_info_error, 'tag': 'system_info'},
        {'class_name': '自定义巡检信息', 'error_count': len(custom_info_data_error),
         'error_info': custom_info_data_error, 'tag': 'custom_info'}
    ]
    inspection_info_detail_sorted = sorted(inspection_info_detail, key=lambda r: r['error_count'], reverse=True)
    inspection_info = {
        'inspection_count': host_results.count(),  # 巡检总指标数
        'inspection_error': host_result_errors.count(),  # 巡检异常数
        'error_percent': int(error_percent),
        # 异常占比
        'error_detail': inspection_info_detail_sorted
    }

    # CPU 物理内存 硬盘空间  inode(使用率）
    host_rate, memory_top = get_obj_by_quota(host_results)

    table_list = [system_config_info, account_config, system_safe, ssh_safe, user_safe, inter_safe, system_run_status,
                  system_performance, custom_info]
    table_list_sorted = sorted(table_list, key=lambda r: r['error_num'] if r else 0, reverse=True)
    table_list_data = [item for item in table_list_sorted if item and len(item['info'])]

    # 将每个信息整合成一个dict
    data_all = {
        'task_host': task_host,
        'inspection_info': inspection_info,
        'host_rate': host_rate,
        'memory_top': memory_top,
        'base_info': base_info,
        'table_list_sorted': table_list_data
    }

    return Request.succFcun(data=data_all)


def do_info_process(data):
    ignore_quota_tag = ['inode_usage', 'disk_usage', 'memory_usage', 'memory_size', 'memory_free', 'cpu_usage',
                        'cpu_top_ten', 'memory_top_ten']
    config_error, all_config = [], []
    for obj in data:
        info_data = {'check_option': obj.quota_id.quota_name, 'check_result': obj.check_result,
                     'recommend_value': obj.recommend_value, 'status': 'true' if obj.result_status else 'false'}
        if obj.quota_id.quota_tag not in ignore_quota_tag:
            all_config.append(info_data)

        if not obj.result_status:
            config_error.append(info_data)
    return config_error, all_config, data[0].system_class.class_name if data else ''


def do_linux_base_info_process(data):
    base_info = []
    for obj in data:
        if obj.quota_id.quota_tag == 'disk_size':
            continue
        info_data = {'check_option': obj.quota_id.quota_name, 'check_result': obj.check_result}
        base_info.append(info_data)
    return base_info


def do_multiple_result_process(obj, flag):
    data = []
    obj_list = obj.split('\n')
    if flag == 'disk':
        for li in obj_list:
            if li:
                li_dict = json.loads(li)
                used_percent = li_dict['IUse'].replace('%', '')
                percent = int(used_percent) / 100 if used_percent else 0
                data.append({'name': li_dict['name'].split('/')[-1], 'percentInt': li_dict['IUse'],
                             'total': li_dict['Avail'], 'free': li_dict['Ifree'], 'percent': percent})
    elif flag == 'inode':
        for li in obj_list:
            if li:
                li_dict = json.loads(li)
                used_percent = li_dict['IUse'].replace('%', '')
                percent = int(used_percent) / 100 if used_percent else 0
                data.append({'name': li_dict['name'].split('/')[-1], 'percentInt': li_dict['IUse'],
                             'total': li_dict['Inodes'], 'free': li_dict['Ifree'], 'percent': percent})

    return data


# 配置信息解析
def analysis_configure_info(host_results):
    safe_config_error, system_run_status_error, system_performance_error, system_info_error, custom_info_data_error, \
    custom_info_data, account_config, system_safe, ssh_safe, user_safe, inter_safe, system_performance_info, \
    system_config_info, system_base_info = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    account_safe_obj, system_safe_obj, ssh_safe_obj, user_safe_obj, inter_safe_obj, system_run_status_info, \
    system_performance_info, system_config_info_data, base_info, custom_info = [], [], [], [], [], [], [], [], [], []
    configure_info_all_dict = {
        '1': system_base_info,  # 基本信息
        '4': account_safe_obj,  # 账号安全
        '6': system_performance_info,  # 系统性能信息
        '7': system_safe_obj,  # 系统安全
        '8': ssh_safe_obj,  # SSH安全设置
        '9': user_safe_obj,  # 用户安全
        '10': system_run_status_info,  # 系统运行状态信息
        '11': inter_safe_obj,  # 网络安全
        '17': system_config_info_data,  # 系统配置信息
        '18': custom_info_data  # 自定义巡检信息
    }

    configure_info_all = host_results.filter(system_class_id__in=[1, 4, 6, 7, 8, 9, 10, 11, 17, 18])
    for configure_info in configure_info_all:
        configure_info_all_dict[str(configure_info.system_class_id)].append(configure_info)

    if system_base_info:
        base_info = do_linux_base_info_process(system_base_info)

    if account_safe_obj:
        config_error, account_config, class_name = do_info_process(account_safe_obj)
        safe_config_error += config_error
        account_config = {'name': class_name, 'error_num': len(config_error), 'info': account_config}

    system_performance = []
    if system_performance_info:
        system_performance_error, system_performance, class_name = do_info_process(system_performance_info)
        system_performance = {'name': class_name, 'error_num': len(system_performance_error),
                              'info': system_performance}

    if system_safe_obj:
        config_error, system_safe, class_name = do_info_process(system_safe_obj)
        safe_config_error += config_error
        system_safe = {'name': class_name, 'error_num': len(config_error), 'info': system_safe}

    if ssh_safe_obj:
        config_error, ssh_safe, class_name = do_info_process(ssh_safe_obj)
        safe_config_error += config_error
        ssh_safe = {'name': class_name, 'error_num': len(config_error), 'info': ssh_safe}

    if user_safe_obj:
        config_error, user_safe, class_name = do_info_process(user_safe_obj)
        safe_config_error += config_error
        user_safe = {'name': class_name, 'error_num': len(config_error), 'info': user_safe}

    system_run_status = []
    if system_run_status_info:
        system_run_status_error, system_run_status, class_name = do_info_process(system_run_status_info)
        system_run_status = {'name': class_name, 'error_num': len(system_run_status_error), 'info': system_run_status}

    if inter_safe_obj:
        config_error, inter_safe, class_name = do_info_process(inter_safe_obj)
        safe_config_error += config_error
        inter_safe = {'name': class_name, 'error_num': len(config_error), 'info': inter_safe}

    if system_config_info_data:
        system_info_error, system_config_info, class_name = do_info_process(system_config_info_data)
        system_config_info = {'name': class_name, 'error_num': len(system_info_error), 'info': system_config_info}

    if custom_info_data:
        custom_info_data_error, custom_info, class_name = do_info_process(custom_info_data)
        custom_info = {'name': class_name, 'error_num': len(custom_info_data_error), 'info': custom_info}

    return safe_config_error, system_run_status_error, system_performance_error, system_info_error, account_config, \
           system_safe, ssh_safe, user_safe, inter_safe, system_run_status, system_performance, system_performance_info, \
           system_config_info, base_info, custom_info_data_error, custom_info


# 特殊处理（cpu ， 物理内存使用率， 硬盘空间使用率，inode使用率）  占用内存TOP10进程
def get_obj_by_quota(host_results):
    cpu_rate, memory_rate, disk_rate, inode_rate, inode_quota, disk_quota, memory_quota, memory_quota_total, \
    memory_quota_free, cpu_quota, top_ten = [], [], [], [], [], [], [], [], [], [], []
    quota_flag = \
        ['inode_usage', 'disk_usage', 'memory_usage', 'memory_size', 'memory_free', 'cpu_usage', 'memory_top_ten']
    info_all_dict = {
        'inode_usage': inode_quota,
        'disk_usage': disk_quota,
        'memory_usage': memory_quota,
        'memory_size': memory_quota_total,
        'memory_free': memory_quota_free,
        'cpu_usage': cpu_quota,
        'memory_top_ten': top_ten
    }

    quota_info_all = Quota.objects.filter(quota_tag__in=quota_flag)
    for info in quota_info_all:
        for obj in host_results.filter(quota_id_id=info.id):
            info_all_dict[info.quota_tag].append(obj)

    if inode_quota:
        inode_rate = do_multiple_result_process(inode_quota[0].check_result, 'inode')
    else:
        inode_rate = [{'name': '', 'percentInt': 0, 'total': '', 'free': '', 'percent': 0}]

    if disk_quota:
        disk_rate = do_multiple_result_process(disk_quota[0].check_result, 'disk')
    else:
        disk_rate = [{'name': '', 'percentInt': 0, 'total': '', 'free': '', 'percent': 0}]

    memory_rate_init = {}
    if memory_quota:
        try:
            memory_rate_init['percentInt'] = float(memory_quota[0].check_result)
        except:
            memory_rate_init['percentInt'] = 0
        memory_rate_init['result_status'] = memory_quota[0].result_status
    if memory_quota_free:
        memory_rate_init['free'] = memory_quota_free[0].check_result
    if memory_quota_total:
        memory_rate_init['total'] = memory_quota_total[0].check_result
    if memory_rate_init:
        memory_rate.append(memory_rate_init)

    if cpu_quota:
        try:
            cpu_rate = [{'percentInt': cpu_quota[0].check_result,
                         'result_status': cpu_quota[0].result_status}]
        except:
            cpu_rate = [{'percentInt': 0, 'result_status': False}]

    host_rate = {
        'cpu': cpu_rate,
        'memory': memory_rate,
        'disk': disk_rate,
        'inode': inode_rate
    }

    # 占用内存TOP10进程
    memory_top = {}
    if top_ten:
        top_obj = top_ten[0].to_dict()
        top_ten_list = top_obj.get('check_result').split('\n')
        process = []  # 进程
        top_value = []  # 进程占用百分比
        process_value = []  # 进程和百分比整合
        for top in top_ten_list[0:11]:
            if top:
                obj = top.split()
                process.append(obj[10].split('/')[-1])
                top_value.append(obj[3])

        for index, pro in enumerate(process):
            process_value.append({'name': pro, 'value': top_value[index]})

        # 内存总数
        memory = '0M'
        if memory_quota_total:
            memory = memory_quota_total[0].check_result

        memory_top = {
            'quota_name': top_obj.get('top_obj'),
            'memory': memory,
            'process': process,
            'processValue': process_value
        }

    return host_rate, memory_top


# window巡检结果详情
def windows_host_detail(req):
    # 根据execute_id获取任务执行历史
    host = req.get("host")
    execute_id = req.get("execute_id")
    # 查询是否有此次日志
    # 任务历史对象
    execute_obj = ExecuteLog.objects.filter(pk=execute_id).first()

    if not execute_obj:
        return Request.errorFcun("巡检报告详情不存在")

    # 基本信息
    execute_dict = execute_obj.to_dict()
    basic_info = {
        # 巡检主机
        "host": host,
        # 开始时间
        "create_time": execute_dict.get("created_time"),
        # 结束时间
        "end_time": execute_dict.get("end_time")
    }

    # 巡检概览信息
    # 查询本次详情
    host_results = TaskHostResult.objects.filter(host_ip=host, execute_log_id=execute_id)
    # 指标总数
    quota_total_num = host_results.count()
    # 异常指标数量
    quota_error_num = host_results.filter(result_status=False).count()

    # 将查询结果转化为 [{}, {}]
    host_result_dicts = [host_result.to_json() for host_result in host_results]
    # 根据system_class_id, system_class_name进行排序
    grouper = itemgetter("system_class_id", "system_class_name", "system_class_sort")
    sorted_host_result_dicts = sorted(host_result_dicts, key=grouper)
    # 根据system_class_id进行分组
    grouped_host_result_dicts = groupby(sorted_host_result_dicts, key=grouper)
    # 指标分类
    quota_class_details = []
    for groupby_field_list, items in grouped_host_result_dicts:
        system_class_id, system_class_name, system_class_sort = groupby_field_list
        temp_quota_error_num = 0
        temp_quota_details = []
        for item in items:
            temp_quota_detail = {
                # 指标名称
                "quota_name": item.get("quota_name"),
                # 指标推荐值
                "recommend_value": item.get("recommend_value"),
                # 检查结果
                "check_result": item.get("check_result"),
                # 结果比对状态
                "result_status": item.get("result_status")
            }
            temp_quota_details.append(temp_quota_detail)
            if not item.get("result_status"):
                temp_quota_error_num += 1
        temp = {
            # 巡检分类id
            "quota_class_id": system_class_id,
            # 巡检分类名称
            "quota_class_name": system_class_name,
            # 巡检分类排序值
            "quota_class_sort": system_class_sort,
            # 巡检分类中异常指标数
            "quota_error_num": temp_quota_error_num,
            # 巡检分类中所有指标详情
            "quota_details": temp_quota_details
        }
        quota_class_details.append(temp)

    # 对指标分类按照异常指标数从大到小进行排序（用户巡检概览TOP4）
    sorted_quota_class_details_by_quota_error_num = sorted(quota_class_details, key=lambda x: x.get("quota_error_num"),
                                                           reverse=True)
    # 截取TOP4
    if len(sorted_quota_class_details_by_quota_error_num) >= 4:
        quota_error_class_top4 = sorted_quota_class_details_by_quota_error_num[:4]
    else:
        quota_error_class_top4 = sorted_quota_class_details_by_quota_error_num

    # 计算异常指标占比（百分比整数）
    if quota_total_num > 0:
        quota_error_percent = int(float(format(float(quota_error_num) / float(quota_total_num), '.2f')) * 100)
    else:
        quota_error_percent = 0
    overview_info = {
        # 巡检总指标数
        "quota_total_num": quota_total_num,
        # 巡检异常指标数
        "quota_error_num": quota_error_num,
        # 异常指标占比
        "quota_error_percent": quota_error_percent,
        # 异常指标分类TOP4
        "quota_error_class_top4": quota_error_class_top4
    }

    # 对指标分类按照数据库设定的排序值进行排序（用于全部展示）
    sorted_quota_class_details_by_quota_class_sort = sorted(quota_class_details,
                                                            key=lambda x: x.get("quota_class_sort"))

    # 处理特殊的指标类
    # 12 磁盘分区信息
    # 5 系统异常服务
    # 14 近七天应用错误日志
    # 16 近七天系统错误日志
    special_system_class_ids = [12, 5, 16, 14]
    for item in sorted_quota_class_details_by_quota_class_sort:
        quota_class_id = item.get("quota_class_id")
        if quota_class_id in special_system_class_ids:
            quota_details = item.get("quota_details")
            if len(quota_details) == 1:
                check_result = quota_details[0].get("check_result")
                try:
                    new_quota_details = json.loads(check_result)
                    if isinstance(new_quota_details, dict):
                        new_quota_details = [new_quota_details]
                except Exception as e:
                    new_quota_details = []
                    error_message = "loads check_result to json failed: %s , result: %s" % (repr(e), check_result)
                    logger.warning(error_message)
                # 磁盘分区信息
                # 盘符输出去掉 :
                # 单位转换 b => GB
                # 计算可用空间百分比
                if quota_class_id in [12]:
                    for new_quota_detail in new_quota_details:
                        device_id = new_quota_detail.get("DeviceID")
                        new_quota_detail["DeviceID"] = device_id.replace(":", "") if device_id else device_id
                        size = new_quota_detail.get("Size")
                        free_space = new_quota_detail.get("FreeSpace")
                        if isinstance(size, int) and isinstance(free_space, int):
                            new_quota_detail["Size"] = round(size / 1024 / 1024 / 1024)
                            new_quota_detail["FreeSpace"] = round(free_space / 1024 / 1024 / 1024)
                            new_quota_detail["FreeSpacePercent"] = int(round(free_space / size, 2) * 100)
                    item["quota_details"] = new_quota_details
                # 近七天应用错误日志、近七天系统错误日志 需要将时间戳格式化为 %Y-%m-%d %H:%M:%S 格式时间, 同时生成统计数据
                elif quota_class_id in [14, 16]:
                    # 定义 EntryType 的映射
                    entry_type_map = {
                        1: "Error",
                        2: "Warning"
                    }
                    # 第一遍遍历，生成 Source 和 Count的映射
                    source_and_count_map = {}
                    for new_quota_detail in new_quota_details:
                        source = new_quota_detail.get("Source")
                        if source:
                            if source not in source_and_count_map:
                                source_and_count_map[source] = 1
                            else:
                                source_and_count_map[source] += 1
                    # 第二遍遍历，格式化TimeGenerated， 插入Count
                    for new_quota_detail in new_quota_details:
                        new_quota_detail["Count"] = source_and_count_map.get(new_quota_detail.get("Source"), 1)
                        new_quota_detail["EntryType"] = entry_type_map.get(new_quota_detail.get("EntryType"),
                                                                           new_quota_detail.get("EntryType"))
                        # time_generated = new_quota_detail.get("TimeGenerated")
                        # try:
                        #     if isinstance(time_generated, str):
                        #         new_time_generated = datetime.datetime.fromtimestamp(
                        #             int(time_generated) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                        #     else:
                        #         new_time_generated = time_generated
                        # except Exception as e:
                        #     new_time_generated = time_generated
                        #     error_message = "format TimeGenerated failed: %s, time_generated: %s" % (repr(e), time_generated)
                        #     logger.warning(error_message)
                        # new_quota_detail["TimeGenerated"] = new_time_generated
                    # 根据Count, TimeGenerated倒序排序
                    sorted_new_quota_details = sorted(new_quota_details, key=lambda x: (x["Count"], x["TimeGenerated"]),
                                                      reverse=True)
                    item["quota_details"] = sorted_new_quota_details
                else:
                    item["quota_details"] = new_quota_details

    data = {
        # 基本信息
        "basic_info": basic_info,
        # 巡检概览
        "overview_info": overview_info,
        # 巡检详情
        "quota_class_details": sorted_quota_class_details_by_quota_class_sort
    }
    return Request.succFcun(data=data)
