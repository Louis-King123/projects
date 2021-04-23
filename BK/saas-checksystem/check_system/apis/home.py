# -*- coding: utf-8 -*-
from django.db.models import Q
from check_system.common import utils
from check_system.common.request import Request
from check_system.models.execute_log import ExecuteLog
from check_system.models.task import Task
from check_system.models.task_result import TaskHostResult
import datetime


def fetch_check_activity(request):
    """
    首页巡检动态接口
    """
    data = []
    # 获取近7条执行完成和执行失败的日志
    execute_logs = ExecuteLog.objects.filter(exec_state__in=[2, 3]).order_by("-end_time").values_list(
        "id", "end_time", "operator", "exec_state", "task_id")[0:7]
    for execute_log in execute_logs:
        execute_log_id, end_time, operator, exec_state, task_id = execute_log
        task = Task.objects.filter(id=task_id).first()
        temp = {
            "id": execute_log_id,
            "tag": "%s" % task.task_name,
            "content": "%s&nbsp;&nbsp;&nbsp;&nbsp;执行人：%s" % (
                end_time.strftime("%Y-%m-%d %H:%M:%S"), operator if operator else "admin"),
            "type": "success" if exec_state == 2 else "danger"
        }
        data.append(temp)
    return Request.succFcun(data=data)


def fetch_check_statistics(request):
    """
    首页巡检统计接口
    """
    start_time = request.GET.get("start_time", datetime.datetime.now().strftime("%Y-%m-%d 00:00:01"))
    end_time = request.GET.get("end_time", datetime.datetime.now().strftime("%Y-%m-%d 23:59:59"))

    # 巡检汇总数据
    # 开始时间结束之间之间的所有执行日志
    execute_logs = ExecuteLog.objects.filter(end_time__range=[start_time, end_time])
    execute_log_ids = execute_logs.values_list("id", flat=True).distinct()
    task_ids = execute_logs.values_list("task_id", flat=True).distinct()
    # 巡检总业务数
    biz_count = Task.objects.filter(id__in=task_ids).values_list("exec_biz_id", flat=True).distinct().count()
    task_host_results = TaskHostResult.objects.filter(execute_log_id__in=execute_log_ids)
    # 巡检主机总数
    total_host_count = task_host_results.values_list("host_ip", flat=True).distinct().count()
    # 巡检总次数
    execute_count = execute_logs.count()
    # 巡检异常主机总数
    error_host_count = task_host_results.filter(result_status=False).values_list("host_ip",
                                                                                 flat=True).distinct().count()
    statistics = {
        # 巡检业务总数
        "biz_count": biz_count,
        # 巡检主机数
        "total_host_count": total_host_count,
        # 巡检总次数
        "execute_count": execute_count,
        # 巡检异常主机数
        "error_host_count": error_host_count
    }

    # 巡检统计数据（折线图）
    # 获取开始结束时间之间所有日期
    date_list = []
    start_date = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        start_date += datetime.timedelta(days=1)
    count_data = {
        "biz_count": [],
        "total_host_count": [],
        "execute_count": [],
        "error_host_count": []
    }
    for date_str in date_list:
        # 每日执行日志
        execute_logs_per_day = ExecuteLog.objects.filter(
            end_time__range=[
                datetime.datetime.strptime(date_str + " 00:00:01", "%Y-%m-%d %H:%M:%S"),
                datetime.datetime.strptime(date_str + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            ]
        )
        # 每日执行日志id列表
        execute_log_ids_per_day = execute_logs_per_day.values_list("id", flat=True).distinct()
        # 每日执行日志涉及的任务列表
        task_ids_per_day = execute_logs_per_day.values_list("task_id", flat=True).distinct()
        # 每日巡检业务数
        biz_count_per_day = Task.objects.filter(id__in=task_ids_per_day).values_list("exec_biz_id",
                                                                                     flat=True).distinct().count()
        task_host_results_per_day = TaskHostResult.objects.filter(execute_log_id__in=execute_log_ids_per_day)
        # 每日巡检主机总数
        total_host_count_per_day = task_host_results_per_day.values_list("host_ip", flat=True).distinct().count()
        # 每日巡检总次数
        execute_count_per_day = execute_logs_per_day.count()
        # 每日巡检异常主机总数
        error_host_count_per_day = task_host_results_per_day.filter(result_status=False).values_list("host_ip",
                                                                                                     flat=True).distinct().count()
        count_data["biz_count"].append(biz_count_per_day)
        count_data["total_host_count"].append(total_host_count_per_day)
        count_data["execute_count"].append(execute_count_per_day)
        count_data["error_host_count"].append(error_host_count_per_day)

    data = {
        "statistics": statistics,
        "reports": {
            # 日期清单（x轴）
            "date_list": date_list,
            # 统计数据（y轴）
            "count_data": count_data
        }
    }
    return Request.succFcun(data=data)
