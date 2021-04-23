# -*- coding: utf-8 -*-

# django imports
import copy
import datetime

from django.db import transaction
from django.http import JsonResponse
#
from django.utils.decorators import method_decorator
from django.views import View

from blueapps.utils.logger import logger
from check_system.common.quota_class import quota_class, tpl_quotas
from check_system.decorator import Log
from check_system.models.models import CheckSystemOs, CheckSystemTplQuta
from check_system.models.tpl import Tpl
from check_system.models.quota import Quota
from check_system.models.task import Task
from check_system.models.task_result import TaskResult
from check_system.common.req import req_body_to_json
from check_system.common.request import Request


def get_os_list(request):
    """
    查询系统列表
    """
    return JsonResponse({
        "result": True,
        "data": [os.to_dict() for os in CheckSystemOs.objects.filter(is_deleted=0).order_by("id")],
        "message": ""
    })


def fetch_tpl_list(request):
    """
    查询巡检模板列表
    """
    os_id = request.GET.get('os_id')
    if os_id:
        data = [tpl.to_dict() for tpl in Tpl.objects.filter(author='system',tpl_os=os_id, is_deleted=0).order_by("-created_time")]
        data.extend([tpl.to_dict() for tpl in Tpl.objects.filter(tpl_os=os_id,is_deleted=0).exclude(author='system').order_by("-created_time")])
        return Request.succFcun(msg="", data=data)
    else:
        data = [tpl.to_dict() for tpl in Tpl.objects.filter(author='system',is_deleted=0).order_by("-created_time")]
        data.extend([tpl.to_dict() for tpl in Tpl.objects.filter(is_deleted=0).exclude(author='system').order_by("-created_time")])
        return Request.succFcun(msg="", data=data)

class Tpl_View(View):
    """
    模板管理
    """
    def get(self, request):
        tpl_id = request.GET.get('tpl_id')
        if not tpl_id:
            return Request.errorFcun("参数异常", data=[])

        # 判断tpl_id是否存在
        tpl_obj = Tpl.objects.filter(id=tpl_id).first()
        if not tpl_obj or tpl_obj.is_deleted == 1:
            return Request.errorFcun("模板不存在", data=[])

        # 根据模板iD 查询模板关联指标中间表
        tpl_quota_list = CheckSystemTplQuta.objects.filter(tpl_id=tpl_obj.id).all()
        # 查询所有关联指标
        quotas = Quota.objects.filter(id__in=[quota.quota_id for quota in tpl_quota_list],is_deleted=0).all()

        data = tpl_obj.to_dict()
        data['tpl_quotas'] = quota_class(quotas,tpl_quota_list)

        return Request.succFcun("sucess", data=data)

    def post(self, request):
        req = req_body_to_json(request)
        tpl_name = req.get("tpl_name", '')
        tpl_os = req.get("tpl_os", '')
        description = req.get("description", '')
        quotas = req.get("quotas", [])

        if not all([tpl_name, tpl_os, len(quotas)]):
            return Request.errorFcun("参数异常", data=[])

        tpl_obj = Tpl.objects.filter(tpl_name=tpl_name,is_deleted=0).first()
        if tpl_obj:
            return Request.errorFcun(msg="添加失败 名称重复", data=[])

        tpl = Tpl(
            tpl_name=tpl_name,
            tpl_os=tpl_os,
            description=description,
            author=request.user.username
        )
        # 批量插入
        if tpl:
            try:
                # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
                with transaction.atomic():
                    tpl.save()

                    # 准备批量插入数据
                    tpl_quota_list_to_insert = list()
                    for quota in quotas:
                        tpl_quota_list_to_insert.append(CheckSystemTplQuta(tpl_id=tpl.id, quota_id=quota['id'],quota_threshold=str(quota['quota_threshold'])))
                    CheckSystemTplQuta.objects.bulk_create(tpl_quota_list_to_insert)

                    field_names = Log.get_model_field(Tpl)
                    field_names['quotas'] = "巡检指标"
                    req['author']=request.user.username
                    req['tpl_os']=CheckSystemOs.objects.get(pk=req['tpl_os']).os_name
                    req['quotas']=tpl_quotas(quotas)
                    Log.operation_log(request,table_name=Tpl._meta.verbose_name,update_fields=req,operation_module_name="模板管理",field_names=field_names)

                    data = req_body_to_json(request)
                    data['tpl_id']= tpl.id
            except:
                logger.error(f"新增模板失败  接口名称({request.path}) 请求参数({req_body_to_json(request)})")

            return Request.succFcun(msg="添加成功", data=data)
        else:
            return Request.errorFcun(msg="添加失败", data=[])

    def put(self, request):
        req = req_body_to_json(request)
        tpl_id = req.get("tpl_id", '')
        tpl_name = req.get("tpl_name", '')
        tpl_os = req.get("tpl_os", '')
        description = req.get("description", '')
        quotas = req.get("quotas", '')

        if not all([tpl_id, tpl_name, tpl_os, len(quotas)]):
            return Request.errorFcun("参数异常", data=[])

        tpl_obj = Tpl.objects.filter(id=tpl_id).first()

        if not tpl_obj:
            return Request.errorFcun(msg="模板不存在", data=[])

        quota_objs = list()

        for quota in quotas:
            # 新添加
            quota_objs.append(CheckSystemTplQuta(tpl_id=tpl_obj.id, quota_id=quota['id'], quota_threshold=str(quota['quota_threshold'])))

        if len(quota_objs):
            # 备份对象用于记录日志
            old_model_obj = copy.deepcopy(tpl_obj)

            # 如果系统更改
            tasks = list()
            if tpl_os != tpl_obj.tpl_os:
                for task in tpl_obj.task_set.all():
                    task.task_os = tpl_os
                    tasks.append(task)

            tpl_obj.tpl_os = tpl_os
            tpl_obj.tpl_name = tpl_name
            tpl_obj.description = description

            try:
                # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
                with transaction.atomic():
                    # 删除旧系统指标
                    CheckSystemTplQuta.objects.filter(tpl_id=tpl_obj.id).delete()
                    # 批量创建新系统指标
                    CheckSystemTplQuta.objects.bulk_create(quota_objs)
                    if tasks:
                        Task.objects.bulk_update(tasks,fields=["task_os"])
                    tpl_obj.save()

                    dict_update_fields = {"tpl_name": tpl_name, "tpl_os": CheckSystemOs.objects.get(pk=tpl_os).os_name,"author": tpl_obj.author, "description": description,
                                          "quotas": tpl_quotas(quotas)}
                    field_names = Log.get_model_field(Tpl)
                    field_names['quotas'] = "巡检指标"
                    Log.operation_log(request, Tpl._meta.verbose_name, old_model_obj, update_fields=dict_update_fields,operation_module_name="模板管理", field_names=field_names)
            except :
                logger.error(f"修改模板失败  接口名称({request.path}) 请求参数({req_body_to_json(request)})")

            return Request.succFcun(msg="修改成功", data=[])
        else:
            return Request.errorFcun(msg="修改失败", data=[])

    def delete(self, request):
        tpl_id = request.GET.get('tpl_id')
        if not tpl_id:
            return Request.errorFcun("参数异常", data=[])

        # 判断tpl_id是否存在
        tpl_obj = Tpl.objects.filter(id=tpl_id).first()

        if not tpl_obj:
            return Request.errorFcun("模板ID不存在", data=[])

        if tpl_obj.is_deleted:
            return Request.succFcun("该模板已删除", data=[])
        else:
            # 备份对象用于记录日志
            old_model_obj = copy.deepcopy(tpl_obj)

            try:
                # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
                with transaction.atomic():
                    # 更改删除状态为1
                    tpl_obj.is_deleted = 1
                    tpl_obj.save()

                    field_names = Log.get_model_field(Tpl)
                    field_names['quotas'] = "巡检指标"
                    Log.operation_log(request,Tpl._meta.verbose_name,old_model_obj,update_fields={},operation_module_name="模板管理",field_names=field_names)

                    # 根据模板iD 查询模板关联指标中间表
                    tpl_quota_list = CheckSystemTplQuta.objects.filter(tpl_id=tpl_obj.id).all()
                    for tpl_quota in tpl_quota_list:
                        tpl_quota.is_deleted = 1
                    CheckSystemTplQuta.objects.bulk_update(tpl_quota_list, fields=['is_deleted'])
            except:
                logger.error(f"删除模板失败  接口名称({request.path}) 请求参数({req_body_to_json(request)})")
            return Request.succFcun("删除成功", data=[])


def execute_tpl(request):
    """
    执行巡检模板
    """

    req = req_body_to_json(request)

    # 获取参数
    tpl_id = req.get("tpl_id", 0)
    ip_list = req.get("ip_list", "")
    # 测试的设置 立即执行
    exec_schedule = req.get("exec_schedule", "instant")

    # 数据校验
    if tpl_id <= 0 or ip_list == "" or exec_schedule == "":
        return JsonResponse({"result": False, "message": "参数错误"})

    # 查询模板
    tpl = Tpl.objects.filter(id=tpl_id)
    if not tpl.exists():
        return JsonResponse({"result": False, "message": "参数错误 找不到这个模板ID"})

    tpl_obj = tpl.first()

    # 模板的指标列表
    tpl_quota_list = eval(tpl_obj.tpl_quotas)

    if len(tpl_quota_list) == 0:
        return JsonResponse({"result": False, "message": "模板的指标是空的，请先添加模板指标"})

    task_obj = Task.objects.create(
        task_name=tpl_obj.tpl_name,
        task_tpl=tpl_obj,
        task_op=request.user.username,
        exec_hosts=ip_list,
        exec_acc="root",  # 此处写死了root，但后期应该修改为可以配置的 因为系统可能是windows，或者有专门的系统用户执行脚本
        exec_schedule=exec_schedule,
        exec_state=0,
        exec_progress=0,
        exec_quota_total=len(tpl_quota_list),
        start_time=datetime.datetime.now(),

        # 通知部分后续考虑
        notify_type="",
        notify_receiver=""
    )

    # exec_schedule的注释
    # 1. instant 立即执行
    # 2. interval 定期执行 示例: interval 5 (表示5秒执行一次)
    # 3. crontab 周期执行 示例: crontab minute hour day_of_week day_of_month month_of_year
    # https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules

    if exec_schedule == "instant":  # 模板任务立即执行
        for quota in Quota.objects.filter(id__in=tpl_quota_list):
            task_result_obj = TaskResult.objects.create(
                task=task_obj,
                quota=quota,
                task_state=0,
                task_step_state=0
            )
            track_task_result.apply_async(args=(task_result_obj,))
    elif exec_schedule.startswith("interval"):
        pass
    elif exec_schedule.startswith("crontab"):
        pass

    return JsonResponse({"result": True})
