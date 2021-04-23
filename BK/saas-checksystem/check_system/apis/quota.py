# -*- coding: utf-8 -*-

import copy
import json

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET

from blueapps.utils.logger import logger
from check_system.common.quota_class import quota_class
from check_system.common.request import Request
from check_system.decorator import Log
from check_system.logic.TplLogic import TplLogic
from check_system.models.check_class import CheckSystemClass
from check_system.models.models import CheckSystemTplQuta, CheckSystemOs
from check_system.models.tpl import Tpl
from check_system.models.quota import Quota
from check_system.common.req import req_body_to_json


def fetch_quota_list(request):
    """
    查询巡检模板列表
    """
    tpl_id = request.GET.get("tpl_id")
    if tpl_id == 0:
        return JsonResponse({"result": False, "message": "参数错误"})

    tpl = Tpl.objects.filter(id=int(tpl_id))
    if not tpl.exists():
        return JsonResponse({"result": False, "message": "参数错误 找不到这个模板ID"})

    # 获取模板对应的指标列表的数组
    tpl_quotas_string = tpl.first().tpl_quotas

    # 查询指标
    tpl_quotas = Quota.objects.filter(id__in=eval(tpl_quotas_string))

    return JsonResponse({
        "result": True,
        "data": [quota.to_dict() for quota in tpl_quotas],
        "message": ""
    })

class Quota_View(View):
    """
    指标接口
    """
    def get(self, request):
        """
        查询系统/模板/自定义 指标
        """
        os_id = request.GET.get("os_id", 0)
        tpl_id = request.GET.get("tpl_id", 0)
        customize = request.GET.get("customize", {})

        # 分页参数
        current = request.GET.get("current", 1)
        limit = request.GET.get("limit", 10)

        if os_id:
            os_id = int(os_id)
            # 根据os_id查询指标
            os_ids = [os_id]
            # 如果是centos 或 Ubuntu 添加99为Linux通用
            if os_id == 1 or os_id == 2:
                os_ids.append(99)
            # 过滤os指标
            quota_query_set = Quota.objects.filter(quota_os__in=os_ids,is_deleted=0)
            quotas = quota_query_set.all()
            return Request.succFcun('', data=quota_class(quotas))

        if tpl_id:
            # 根据tpl_id查询指标
            tpl = Tpl.objects.filter(id=int(tpl_id), is_deleted=0)
            if not tpl.exists():
                return Request.errorFcun('模板不存在')

            # 根据模板iD 查询模板关联指标中间表
            tpl_quota_list = CheckSystemTplQuta.objects.filter(tpl_id=tpl_id).all()
            # 查询模板关联指标
            quotas = Quota.objects.filter(id__in=[quota.quota_id for quota in tpl_quota_list]).all()
            return Request.succFcun('', data=quota_class(quotas, tpl_quota_list))

        # 查询巡检项
        if customize:
            kwargs = json.loads(customize)
            # 如果存在指标名 变为模糊查询指标
            if 'quota_name' in kwargs:
                kwargs['quota_name__icontains'] = kwargs.pop('quota_name')

            # 删除空值项
            for key_str in list(kwargs.keys()):
                if not kwargs[key_str]:
                    kwargs.pop(key_str)

            # 查询指标
            quotas = Quota.objects.filter(**kwargs)
            paginator = Paginator(quotas.order_by("quota_os", "id", "-created_time"), int(limit))
            data = [quota.to_dict() for quota in paginator.page(int(current))]
            return Request.succFcun('', data={"count":paginator.count,"data":data})


    def post(self, request):
        req = req_body_to_json(request)
        quota_name = req.get("quota_name", "")
        quota_os = req.get("quota_os", 0)
        script_type = req.get("script_type", "")
        script_content = req.get("script_content", "")

        quota_handler = req.get("quota_handler", "cmp_show")
        quota_threshold = req.get("quota_threshold", "")
        username = req.get("username", "")

        if not all([quota_name, username, quota_os, script_type, script_content]):
            return Request.errorFcun("参数异常", data=[])

        quota_obj = Quota.objects.filter(quota_name=quota_name, is_deleted=0).first()
        if quota_obj:
            return Request.errorFcun(msg="添加失败 名称重复", data=[])

        quota = Quota(
            quota_name=quota_name,
            quota_os=quota_os,
            script_type=script_type,
            script_content=script_content,
            quota_handler=quota_handler,
            quota_threshold=quota_threshold,
            author=username,
            quota_class=18,
        )
        if quota:
            try:
                # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
                with transaction.atomic():
                    quota.save()
                    field_names = Log.get_model_field(Quota)
                    req['author']=username
                    req['quota_os']=CheckSystemOs.objects.get(pk=quota_os).os_name
                    req['quota_class'] = "自定义巡检"
                    Log.operation_log(request,table_name=Quota._meta.verbose_name,update_fields=req,operation_module_name="自定义巡检",field_names=field_names)
            except:
                logger.error(f"新增自定义巡检失败  接口名称({request.path}) 请求参数({req_body_to_json(request)})")
            return Request.succFcun(msg="添加成功", data=[])
        else:
            return Request.errorFcun(msg="添加失败", data=[])

    def put(self, request):
        req = req_body_to_json(request)
        quota_id = req.get("quota_id", 0)
        quota_name = req.get("quota_name", "")
        quota_os = req.get("quota_os", 0)
        script_type = req.get("script_type", "")
        script_content = req.get("script_content", "")
        quota_handler = req.get("quota_handler", "cmp_show")
        quota_threshold = req.get("quota_threshold", "")

        if not all([quota_id, quota_name, quota_os, script_type, script_content, quota_handler]):
            return Request.errorFcun("参数异常", data=[])

        # 如果设置了对比方式 但未设置值
        if quota_handler != "cmp_show" and not quota_threshold:
            return Request.errorFcun("请设置阈值", data=[])

        # 判断是否存在
        quota_obj = Quota.objects.filter(id=quota_id)
        if quota_obj.exists():
            quota = Quota.objects.get(pk=quota_id)
            try:
                # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
                with transaction.atomic():
                    req.pop("quota_id")
                    Quota.objects.filter(id=quota_id).update(**req)

                    field_names = Log.get_model_field(Quota)
                    req['quota_threshold']= quota.quota_threshold
                    req['author'] = quota.author
                    req['quota_os'] = CheckSystemOs.objects.get(pk=quota.quota_os).os_name
                    req['quota_class'] = CheckSystemClass.objects.get(pk=quota.quota_class).class_name

                    Log.operation_log(request,Quota._meta.verbose_name,quota,update_fields=req,operation_module_name="自定义巡检",field_names=field_names)
            except:
                logger.error(f"修改自定义巡检失败  接口名称({request.path}) 请求参数({req_body_to_json(request)})")
            return Request.succFcun(msg="修改成功", data=[])
        else:
            return Request.errorFcun(msg="修改失败", data=[])

    def delete(self, request):
        quota_id = request.GET.get('quota_id')
        if not quota_id:
            return Request.errorFcun("参数异常", data=[])

        # 判断是否存在
        quota_obj = Quota.objects.filter(id=quota_id)
        if not quota_obj.exists():
            return Request.errorFcun("指标不存在", data=[])

        # 判断是否存在模板关联关系
        tpl_quota = CheckSystemTplQuta.objects.filter(quota_id=quota_id,is_deleted=0)
        if tpl_quota.exists():
            return Request.succFcun("删除失败，与模板存在关联关系", data=[])

        quota = quota_obj.first()

        if quota.is_deleted:
            return Request.succFcun("该指标已删除", data=[])
        else:
            # 备份对象用于记录日志
            old_model_obj = copy.deepcopy(quota)
            try:
                # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
                with transaction.atomic():
                    # 更改删除状态为1
                    quota.is_deleted = 1
                    quota.save()

                    field_names = Log.get_model_field(Quota)
                    Log.operation_log(request,Quota._meta.verbose_name,old_model_obj,update_fields={},operation_module_name="自定义巡检",field_names=field_names)
            except:
                logger.error(f"删除自定义巡检失败  接口名称({request.path}) 请求参数({dict(request.GET)})")
            return Request.succFcun("删除成功", data=[])


def add_quota(request):
    """
    添加模板指标
    """
    req = req_body_to_json(request)

    # 获取参数
    tpl_id = req.get("tpl_id", 0)
    quota_name = req.get("quota_name", "")
    script_type = req.get("script_type", 0)
    script_content = req.get("script_content", "")
    quota_handler = req.get("quota_handler", "")
    quota_threshold = req.get("quota_threshold", "")

    # 数据校验
    if tpl_id <= 0 or quota_name == "" or \
            script_type <= 0 or script_content == "" or \
            quota_handler == "" or quota_threshold == "":
        return JsonResponse({"result": False, "message": "参数错误"})

    # 查询模板
    tpl = Tpl.objects.filter(id=tpl_id)
    if not tpl.exists():
        return JsonResponse({"result": False, "message": "参数错误 找不到这个模板ID"})

    tpl_obj = tpl.first()

    # 判断指标名字是否存在 (区分操作系统)
    if Quota.objects.filter(quota_name=quota_name, quota_os=tpl_obj.tpl_os).exists():
        return JsonResponse({"result": False, "message": "这个操作系统[" + tpl_obj.tpl_os + "]已经有这个名字的指标了"})

    quota = Quota.objects.create(
        quota_name=quota_name,
        quota_os=tpl_obj.tpl_os,
        quota_handler=quota_handler,
        quota_threshold=quota_threshold,
        script_type=script_type,
        script_content=script_content,
    )

    # 查模板之前的指标
    tpl_quota_list = eval(tpl_obj.tpl_quotas)
    # 简易去重
    tpl_quota_set = set(tpl_quota_list)
    tpl_quota_set.add(quota.id)

    # 模板添加刚刚创建的指标
    tpl.update(tpl_quotas=json.dumps(list(tpl_quota_set)))

    return JsonResponse({"code": 0, "msg": "添加成功", "data": []})


def fetch_quota_by_tpl(request):
    """
    根据tpl查询指标
    """
    tpl_id = request.GET.get("tpl_id", 0)
    if tpl_id == 0:
        return Request.errorFcun('参数错误')

    tpl = Tpl.objects.filter(id=int(tpl_id))
    if not tpl.exists():
        return Request.errorFcun('模板不存在')

    tplLogic = TplLogic()
    data = tplLogic.getQuotas(tpl_id)
    return Request.succFcun('', data)


@require_GET
def fetch_os_quota(request):
    """
    查询符合系统的指标
    """
    os_id = request.GET.get("os_id", 0)
    if not os_id:
        return Request.errorFcun(msg="参数错误")

    # 查询指标 系统id,通用id
    quotas = Quota.objects.filter(quota_os__in=[os_id, 99]).all()

    return Request.succFcun(data=quota_class(quotas))
