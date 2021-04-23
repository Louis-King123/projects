# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import BaseSoftData
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat, batch_verification


@require_http_methods(["POST"])
def fetch_base_soft_list(request):
    """
    获取基础软件实例列表数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    base_soft_id = req_params.get("id")
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("sJorgCode")
    sj_soft_name = req_params.get("sJsoftName")
    is_reported = req_params.get("isReported")
    sj_soft_type = req_params.get("sJsoftType")  # 软件类型1.数据库；2.中间件；9.其他
    create_time_range = req_params.get("createTimeRange")
    update_time_range = req_params.get("updateTimeRange")

    try:
        base_soft_list = BaseSoftData.objects.filter(isDeleted=0).order_by("-id")
        vd_res = is_data_validation_defeat('id', base_soft_id, 'not_none')
        if not vd_res:
            base_soft_list = base_soft_list.filter(id=base_soft_id)
        vd_res = is_data_validation_defeat('sj_soft_name', sj_soft_name, 'not_none')
        if not vd_res:
            base_soft_list = base_soft_list.filter(sJsoftName__contains=sj_soft_name)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            base_soft_list = base_soft_list.filter(sJorgCode=sj_org_code)
        vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_none')
        if not vd_res:
            base_soft_list = base_soft_list.filter(isReported=is_reported)
        vd_res = is_data_validation_defeat('sj_soft_type', sj_soft_type, 'not_none')
        if not vd_res:
            base_soft_list = base_soft_list.filter(sJsoftType=sj_soft_type)
        if update_time_range is not None and len(update_time_range) == 2:
            satm = update_time_range[0]
            edtm = update_time_range[1]
            base_soft_list = base_soft_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            base_soft_list = base_soft_list.filter(createdTime__range=(satm, edtm))
        current_page = get_actual_page(len(base_soft_list), limit, current_page)
        paginator = Paginator(base_soft_list, limit)
        base_soft_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if base_soft_list:
            for item in base_soft_list:
                data_list.append({
                    "id": item.id,
                    "sJorgCode": item.sJorgCode,
                    "sJsoftType": item.sJsoftType,
                    "sJsoftName": item.sJsoftName,
                    "sJsoftVersion": item.sJsoftVersion,
                    "sJsoftIp": item.sJsoftIp,
                    "sJsoftPort": item.sJsoftPort,
                    "isReported": item.isReported,
                    "isDeleted": item.isDeleted,
                    "sJsortCode": None,
                    "createdTime": item.createdTime.strftime("%Y-%m-%d %H:%M:%S") if item.createdTime else None,
                    "updatedTime": item.updatedTime.strftime("%Y-%m-%d %H:%M:%S"),
                })
            data = {
                'count': paginator.count,
                'list': data_list,
                'current_page': current_page
            }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def update_base_soft(request):
    """
    更新基础软件实例数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    base_soft_id = req_params.get("id")
    sj_org_code = req_params.get("sJorgCode")  # 公安机关机构代码
    sj_soft_type = req_params.get("sJsoftType")  # 软件类型1.数据库；2.中间件；9.其他
    sj_soft_name = req_params.get("sJsoftName")
    sj_soft_version = req_params.get("sJsoftVersion")
    sj_soft_ip = req_params.get("sJsoftIp")
    sj_soft_port = req_params.get("sJsoftPort")
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    vd_res = is_data_validation_defeat('id', base_soft_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        base_soft_data = BaseSoftData.objects.filter(id=base_soft_id).first()
        if not base_soft_data:
            return json_resp("编辑失败", None, 500)
        if sj_org_code is not None:
            base_soft_data.sJorgCode = sj_org_code
        if sj_soft_type is not None:
            vd_res = is_data_validation_defeat('sj_soft_type', sj_soft_type, 'not_in', [1, 2, 9])
            if vd_res:
                return json_resp(vd_res, None, 500)
            base_soft_data.sJsoftType = sj_soft_type
        if sj_soft_name is not None:
            vd_res = is_data_validation_defeat('sj_soft_name', sj_soft_name, 'not_none')
            if vd_res:
                return json_resp(vd_res, None, 500)
            base_soft_data.sJsoftName = sj_soft_name
        if sj_soft_version is not None:
            base_soft_data.sJsoftVersion = sj_soft_version
        if sj_soft_ip is not None:
            base_soft_data.sJsoftIp = sj_soft_ip
        if sj_soft_port is not None:
            base_soft_data.sJsoftPort = sj_soft_port
        if is_reported is not None:
            vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            base_soft_data.isReported = is_reported
        if is_deleted is not None:
            vd_res = is_data_validation_defeat('is_deleted', is_deleted, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            base_soft_data.isDeleted = is_reported
        base_soft_data.createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        base_soft_data.updatedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        base_soft_data.save()
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def add_base_soft(request):
    """
    新增基础软件实例数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    sj_org_code = req_params.get("sJorgCode")  # 公安机关机构代码
    sj_soft_type = req_params.get("sJsoftType")  # 软件类型1.数据库；2.中间件；9.其他
    sj_soft_name = req_params.get("sJsoftName")
    sj_soft_version = req_params.get("sJsoftVersion")
    sj_soft_ip = req_params.get("sJsoftIp")
    sj_soft_port = req_params.get("sJsoftPort")
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    try:
        configs = [
            {"key": "sJorgCode", "value": sj_org_code, "v_type": "not_none"},
            {"key": "sJsoftType", "value": sj_soft_type, "v_type": "not_none"},
            {"key": "sJsoftName", "value": sj_soft_name, "v_type": "not_none"},
            {"key": "sJsoftVersion", "value": sj_soft_version, "v_type": "not_none"},
            {"key": "sJsoftIp", "value": sj_soft_ip, "v_type": "not_none"},
            {"key": "sJsoftPort", "value": sj_soft_port, "v_type": "not_none"},
        ]
        res_obj = batch_verification(configs)
        if res_obj.get("msg") != "success":
            return json_resp(res_obj.get("msg"), None, 500)
        BaseSoftData.objects.create(
            sJorgCode=sj_org_code,
            sJsoftType=sj_soft_type,
            sJsoftName=sj_soft_name,
            sJsoftVersion=sj_soft_version,
            sJsoftIp=sj_soft_ip,
            sJsoftPort=sj_soft_port,
            isReported=0,
            isDeleted=0,
            createdTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            updatedTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def delete_base_soft(request):
    """
    批量删除基础软件实例数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    ids = req_params.get("ids")
    try:
        vd_res = is_data_validation_defeat('ids', ids, 'is_list')
        if vd_res:
            return json_resp(vd_res, None, 500)
        BaseSoftData.objects.filter(id__in=ids).update(isDeleted=1)
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)



