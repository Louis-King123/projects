# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import CloudServeType
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat, batch_verification


@require_http_methods(["POST"])
def fetch_cloud_serve_type_list(request):
    """
    获取云平台分服务类型建设情况数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("sJorgCode")
    cloud_serve_type_id = req_params.get("id")
    sj_cloud_serv_name = req_params.get("sJcloudServName")
    create_time_range = req_params.get("createTimeRange")
    update_time_range = req_params.get("updateTimeRange")
    is_reported = req_params.get("isReported")
    try:
        cloud_serve_type_list = CloudServeType.objects.filter(isDeleted=0).order_by("-id")
        if update_time_range is not None and len(update_time_range) == 2:
            satm = update_time_range[0]
            edtm = update_time_range[1]
            cloud_serve_type_list = cloud_serve_type_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            cloud_serve_type_list = cloud_serve_type_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('sj_cloud_serv_name', sj_cloud_serv_name, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(sJcloudServName__contains=sj_cloud_serv_name)
        vd_res = is_data_validation_defeat('id', cloud_serve_type_id, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(id=cloud_serve_type_id)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(sJorgCode=sj_org_code)
        vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(isReported=is_reported)
        current_page = get_actual_page(len(cloud_serve_type_list), limit, current_page)
        paginator = Paginator(cloud_serve_type_list, limit)
        cloud_serve_type_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if cloud_serve_type_list:
            for item in cloud_serve_type_list:
                data_list.append({
                    "id": item.id,
                    "sJorgCode": item.sJorgCode,
                    "sJcloudServType": item.sJcloudServType,
                    "sJcloudServName": item.sJcloudServName,
                    "sJcloudServCode": item.sJcloudServCode,
                    "sJcloudcount": item.sJcloudcount,
                    "sJcloudBrandCpu": item.sJcloudBrandCpu,
                    "sJcloudBrandMem": item.sJcloudBrandMem,
                    "sJcloudBrandStore": item.sJcloudBrandStore,
                    "sJcloudBrandBand": item.sJcloudBrandBand,
                    "isReported": item.isReported,
                    "isDeleted": item.isDeleted,
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
def update_cloud_serve_type(request):
    """
    编辑云平台分服务类型建设情况
    :param request:
    :return:
    """
    req_params = parse_json(request)
    cloud_serve_type_id = req_params.get("id")
    sj_org_code = req_params.get("sJorgCode")  # 公安机关机构代码
    sj_cloud_serv_type = req_params.get("sJcloudServType")
    sj_cloud_serv_name = req_params.get("sJcloudServName")
    sj_cloud_serv_code = req_params.get("sJcloudServCode")
    sj_cloud_count = req_params.get("sJcloudcount")
    sj_cloud_brand_cpu = req_params.get("sJcloudBrandCpu")
    sj_cloud_brand_mem = req_params.get("sJcloudBrandMem")
    sj_cloud_brand_store = req_params.get("sJcloudBrandStore")
    sj_cloud_brand_band = req_params.get("sJcloudBrandBand")
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    vd_res = is_data_validation_defeat('id', cloud_serve_type_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        cloud_serve_type = CloudServeType.objects.filter(id=cloud_serve_type_id).first()
        if not cloud_serve_type:
            return json_resp("编辑失败", None, 500)
        if sj_org_code is not None:
            cloud_serve_type.sJorgCode = sj_org_code
        if sj_cloud_serv_type is not None:
            cloud_serve_type.sJcloudServType = sj_cloud_serv_type
        if sj_cloud_serv_name is not None:
            cloud_serve_type.sJcloudServName = sj_cloud_serv_name
        if sj_cloud_serv_code is not None:
            cloud_serve_type.sJcloudServCode = sj_cloud_serv_code
        if sj_cloud_count is not None:
            vd_res = is_data_validation_defeat('sj_cloud_count', sj_cloud_count, 'not_none')
            if vd_res:
                return json_resp(vd_res, None, 500)
            cloud_serve_type.sJcloudcount = sj_cloud_count
        if sj_cloud_brand_cpu is not None:
            vd_res = is_data_validation_defeat('sj_cloud_brand_cpu', sj_cloud_brand_cpu, 'not_none')
            if vd_res:
                return json_resp(vd_res, None, 500)
            cloud_serve_type.sJcloudBrandCpu = sj_cloud_brand_cpu
        if sj_cloud_brand_mem is not None:
            vd_res = is_data_validation_defeat('sj_cloud_brand_mem', sj_cloud_brand_mem, 'not_none')
            if vd_res:
                return json_resp(vd_res, None, 500)
            cloud_serve_type.sJcloudBrandMem = sj_cloud_brand_mem
        if sj_cloud_brand_store is not None:
            vd_res = is_data_validation_defeat('sj_cloud_brand_store', sj_cloud_brand_store, 'not_none')
            if vd_res:
                return json_resp(vd_res, None, 500)
            cloud_serve_type.sJcloudBrandStore = sj_cloud_brand_store
        if sj_cloud_brand_band is not None:
            vd_res = is_data_validation_defeat('sj_cloud_brand_band', sj_cloud_brand_band, 'not_none')
            if vd_res:
                return json_resp(vd_res, None, 500)
            cloud_serve_type.sJcloudBrandBand = sj_cloud_brand_band
        if is_reported is not None:
            vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            cloud_serve_type.isReported = is_reported
        if is_deleted is not None:
            vd_res = is_data_validation_defeat('is_deleted', is_deleted, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            cloud_serve_type.isDeleted = is_reported
        cloud_serve_type.createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cloud_serve_type.updatedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cloud_serve_type.save()
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def delete_cloud_serve_type(request):
    """
    批量删除云平台分服务类型建设情况
    :param request:
    :return:
    """
    req_params = parse_json(request)
    ids = req_params.get("ids")
    try:
        vd_res = is_data_validation_defeat('ids', ids, 'is_list')
        if vd_res:
            return json_resp(vd_res, None, 500)
        CloudServeType.objects.filter(id__in=ids).update(isDeleted=1)
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def add_cloud_serve_type(request):
    """
    新增云平台分服务类型建设情况
    :param request:
    :return:
    """
    req_params = parse_json(request)
    sj_org_code = req_params.get("sJorgCode")  # 公安机关机构代码
    sj_cloud_serv_type = req_params.get("sJcloudServType")
    sj_cloud_serv_name = req_params.get("sJcloudServName")
    sj_cloud_serv_code = req_params.get("sJcloudServCode")
    sj_cloud_count = req_params.get("sJcloudcount")
    sj_cloud_brand_cpu = req_params.get("sJcloudBrandCpu")
    sj_cloud_brand_mem = req_params.get("sJcloudBrandMem")
    sj_cloud_brand_store = req_params.get("sJcloudBrandStore")
    sj_cloud_brand_band = req_params.get("sJcloudBrandBand")
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    try:
        configs = [
            {"key": "sJorgCode", "value": sj_org_code, "v_type": "not_none"},
            {"key": "sJcloudServType", "value": sj_cloud_serv_type, "v_type": "not_none"},
            {"key": "sJcloudServName", "value": sj_cloud_serv_name, "v_type": "not_none"},
            {"key": "sJcloudServCode", "value": sj_cloud_serv_code, "v_type": "not_none"},
            {"key": "sJcloudcount", "value": sj_cloud_count, "v_type": "not_none"},
            {"key": "sJcloudBrandCpu", "value": sj_cloud_brand_cpu, "v_type": "not_none"},
            {"key": "sJcloudBrandMem", "value": sj_cloud_brand_mem, "v_type": "not_none"},
            {"key": "sJcloudBrandStore", "value": sj_cloud_brand_store, "v_type": "not_none"},
            {"key": "sJcloudBrandBand", "value": sj_cloud_brand_band, "v_type": "not_none"},

        ]
        res_obj = batch_verification(configs)
        if res_obj.get("msg") != "success":
            return json_resp(res_obj.get("msg"), None, 500)
        CloudServeType.objects.create(
            sJorgCode=sj_org_code,
            sJcloudServType=sj_cloud_serv_type,
            sJcloudServName=sj_cloud_serv_name,
            sJcloudServCode=sj_cloud_serv_code,
            sJcloudcount=sj_cloud_count,
            sJcloudBrandCpu=sj_cloud_brand_cpu,
            sJcloudBrandMem=sj_cloud_brand_mem,
            sJcloudBrandStore=sj_cloud_brand_store,
            sJcloudBrandBand=sj_cloud_brand_band,
            isReported=0,
            isDeleted=0,
            createdTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            updatedTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)
