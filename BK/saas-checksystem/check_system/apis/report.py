# -*- coding: utf-8 -*-

from django.http import JsonResponse

from check_system.common.req import req_body_to_json
from check_system.models.task import Task
from check_system.models.task_result import TaskResult


def fetch_report(request):
    """
    查询报告
    """

    req = req_body_to_json(request)

    # 获取参数
    task_id = req.get("task_id", 0)

    # task_id = request.GET.get("task_id", 0)

    # 数据校验
    if int(task_id) <= 0:
        return JsonResponse({"result": False, "message": "参数错误"})

    task = Task.objects.filter(id=task_id)
    if not task.exists():
        return JsonResponse({"result": False, "message": "没有查询到这个任务"})

    task = task.first()

    task_result_list = []
    for tr in TaskResult.objects.filter(task=task):
        task_result_dict = tr.to_dict()

        task_result_temp = {
            "quota_name": task_result_dict["quota_name"],
            "task_state": task_result_dict["task_state"],
            "task_step_state": task_result_dict["task_step_state"],
            "result": [],
        }
        if task_result_dict["result"]:
            for ip, val in task_result_dict["result"].items():
                temp = {
                    "ip": ip,
                    "val": val[task_result_dict["quota_name"]],
                    "threshold": task_result_dict["quota_threshold"],
                }
                warn_name = task_result_dict["quota_name"] + "_warning"
                if val.get(warn_name, False):
                    temp["warning"] = val[task_result_dict["quota_name"] + "_warning"]

                show_name = task_result_dict["quota_name"] + "_show"
                if val.get(show_name, False):
                    temp["show"] = val[task_result_dict["quota_name"] + "_show"]

                task_result_temp["result"].append(temp)

        task_result_list.append(task_result_temp)

    return JsonResponse({
        "result": True,
        "data": task_result_list,
        "message": ""
    })
