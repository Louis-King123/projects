# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import CloudDataAll
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat, batch_verification


@require_http_methods(["POST"])
def fetch_cloud_data_list(request):
    """
    获取云平台总体建设情况数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    cloud_data_id = req_params.get("id")
    sj_org_code = req_params.get("sJorgCode")
    create_time_range = req_params.get("createTimeRange")
    update_time_range = req_params.get("updateTimeRange")
    is_reported = req_params.get("isReported")
    try:
        cloud_data_list = CloudDataAll.objects.filter(isDeleted=0).order_by("-id")
        if update_time_range is not None and len(update_time_range) == 2:
            satm = update_time_range[0]
            edtm = update_time_range[1]
            cloud_data_list = cloud_data_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            cloud_data_list = cloud_data_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('id', cloud_data_id, 'not_none')
        if not vd_res:
            cloud_data_list = cloud_data_list.filter(id=cloud_data_id)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            cloud_data_list = cloud_data_list.filter(sJorgCode=sj_org_code)
        vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_none')
        if not vd_res:
            cloud_data_list = cloud_data_list.filter(isReported=is_reported)
        current_page = get_actual_page(len(cloud_data_list), limit, current_page)
        paginator = Paginator(cloud_data_list, limit)
        cloud_data_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if cloud_data_list:
            for item in cloud_data_list:
                data_list.append({
                    "id": item.id,
                    "sJorgCode": item.sJorgCode,
                    "sJvmPlatCode": item.sJvmPlatCode,
                    "sJcloudBrand": item.sJcloudBrand,
                    "sJcloudScale": item.sJcloudScale,
                    "sJcloudServCount": item.sJcloudServCount,
                    "sJcloudServTypes": item.sJcloudServTypes,
                    "sJcloudAppCount": item.sJcloudAppCount,
                    "isReported": item.isReported,
                    "isDeleted": item.isDeleted,
                    "createdTime": item.createdTime.strftime("%Y-%m-%d %H:%M:%S") if item.createdTime else None,
                    "updatedTime": item.updatedTime.strftime("%Y-%m-%d %H:%M:%S")
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
def update_cloud_data(request):
    """
    编辑云平台总体建设情况数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    cloud_data_id = req_params.get("id")
    sj_org_code = req_params.get("sJorgCode")  # 公安机关机构代码
    sj_vm_plat_code = req_params.get("sJvmPlatCode")
    sj_cloud_brand = req_params.get("sJcloudBrand")
    sj_cloud_scale = req_params.get("sJcloudScale")
    sj_cloud_serv_count = req_params.get("sJcloudServCount")
    sj_cloud_serv_types = req_params.get("sJcloudServTypes")
    sj_cloud_app_count = req_params.get("sJcloudAppCount")
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    vd_res = is_data_validation_defeat('id', cloud_data_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        cloud_data = CloudDataAll.objects.filter(id=cloud_data_id).first()
        if not cloud_data:
            return json_resp("编辑失败", None, 500)
        if sj_org_code is not None:
            cloud_data.sJorgCode = sj_org_code
        if sj_vm_plat_code is not None:
            cloud_data.sJvmPlatCode = sj_vm_plat_code
        if sj_cloud_brand is not None:
            cloud_data.sJcloudBrand = sj_cloud_brand
        if sj_cloud_scale is not None:
            vd_res = is_data_validation_defeat('sj_cloud_scale', sj_cloud_scale, 'not_none')
            if not vd_res:
                cloud_data.sJcloudScale = sj_cloud_scale
            else:
                return json_resp(vd_res, None, 500)
        if sj_cloud_serv_count is not None:
            vd_res = is_data_validation_defeat('sj_cloud_serv_count', sj_cloud_serv_count, 'not_none')
            if not vd_res:
                cloud_data.sJcloudServCount = sj_cloud_serv_count
            else:
                return json_resp(vd_res, None, 500)
        if sj_cloud_serv_types is not None:
            cloud_data.sJcloudServTypes = sj_cloud_serv_types
        if sj_cloud_app_count is not None:
            vd_res = is_data_validation_defeat('sj_cloud_app_count', sj_cloud_app_count, 'not_none')
            if not vd_res:
                cloud_data.sJcloudAppCount = sj_cloud_app_count
            else:
                return json_resp(vd_res, None, 500)
        if is_reported is not None:
            vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_in', [1, 0])
            if not vd_res:
                cloud_data.isReported = is_reported
            else:
                return json_resp(vd_res, None, 500)
        if is_deleted is not None:
            vd_res = is_data_validation_defeat('is_deleted', is_deleted, 'not_in', [1, 0])
            if not vd_res:
                cloud_data.isDeleted = is_reported
            else:
                return json_resp(vd_res, None, 500)
        cloud_data.createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cloud_data.updatedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cloud_data.save()
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def delete_cloud_data(request):
    """
    批量删除云平台总体建设情况数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    ids = req_params.get("ids")
    try:
        vd_res = is_data_validation_defeat('ids', ids, 'is_list')
        if vd_res:
            return json_resp(vd_res, None, 500)
        CloudDataAll.objects.filter(id__in=ids).update(isDeleted=1)
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def add_cloud_data(request):
    """
    新增云平台总体建设情况
    :param request:
    :return:
    """
    req_params = parse_json(request)
    sj_org_code = req_params.get("sJorgCode")  # 公安机关机构代码
    sj_vm_plat_code = req_params.get("sJvmPlatCode")
    sj_cloud_brand = req_params.get("sJcloudBrand")
    sj_cloud_scale = req_params.get("sJcloudScale")
    sj_cloud_serv_count = req_params.get("sJcloudServCount")
    sj_cloud_serv_types = req_params.get("sJcloudServTypes")
    sj_cloud_app_count = req_params.get("sJcloudAppCount")
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    try:
        configs = [
            {"key": "sJorgCode", "value": sj_org_code, "v_type": "not_none"},
            {"key": "sJvmPlatCode", "value": sj_vm_plat_code, "v_type": "not_none"},
            {"key": "sJcloudBrand", "value": sj_cloud_brand, "v_type": "not_none"},
            {"key": "sJcloudScale", "value": sj_cloud_scale, "v_type": "not_none"},
            {"key": "sJcloudServCount", "value": sj_cloud_serv_count, "v_type": "not_none"},
            {"key": "sJcloudServTypes", "value": sj_cloud_serv_types, "v_type": "not_none"},
            {"key": "sJcloudAppCount", "value": sj_cloud_app_count, "v_type": "not_none"},

        ]
        res_obj = batch_verification(configs)
        if res_obj.get("msg") != "success":
            return json_resp(res_obj.get("msg"), None, 500)
        CloudDataAll.objects.create(
            sJorgCode=sj_org_code,
            sJvmPlatCode=sj_vm_plat_code,
            sJcloudBrand=sj_cloud_brand,
            sJcloudScale=sj_cloud_scale,
            sJcloudServCount=sj_cloud_serv_count,
            sJcloudServTypes=sj_cloud_serv_types,
            sJcloudAppCount=sj_cloud_app_count,
            isReported=0,
            isDeleted=0,
            createdTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            updatedTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)
