# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import ServerData
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat, set_attr_by_data_valid


@require_http_methods(["POST"])
def fetch_server_data_list(request):
    """
    获取服务器检测指标数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    create_time_range = req_params.get("createTimeRange")
    update_time_range = req_params.get("updateTimeRange")
    server_data_id = req_params.get("id")
    sj_org_code = req_params.get("orgCode")
    is_reported = req_params.get("isReported")
    dev_online_state = req_params.get("devOnlineState")
    dev_alert_level = req_params.get("devAlertLevel")
    try:
        server_data_list = ServerData.objects.filter(isDeleted=0).order_by("-id")
        if update_time_range is not None and len(update_time_range):
            satm = update_time_range[0]
            edtm = update_time_range[1]
            server_data_list = server_data_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            server_data_list = server_data_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('id', server_data_id, 'not_none')
        if not vd_res:
            server_data_list = server_data_list.filter(id=server_data_id)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            server_data_list = server_data_list.filter(orgCode=sj_org_code)
        vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_none')
        if not vd_res:
            server_data_list = server_data_list.filter(isReported=is_reported)
        vd_res = is_data_validation_defeat('devOnlineState', dev_online_state, 'not_none')
        if not vd_res:
            server_data_list = server_data_list.filter(devOnlineState=dev_online_state)
        vd_res = is_data_validation_defeat('devAlertLevel', dev_alert_level, 'not_none')
        if not vd_res:
            server_data_list = server_data_list.filter(devAlertLevel=dev_alert_level)
        current_page = get_actual_page(len(server_data_list), limit, current_page)
        paginator = Paginator(server_data_list, limit)
        server_data_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if server_data_list:
            for item in server_data_list:
                data_list.append({
                    "id": item.id,
                    "orgCode": item.orgCode,
                    "ciId": item.ciId,
                    "devOnlineState": item.devOnlineState,
                    "devResponseTime": item.devResponseTime,
                    "devAlertLevel": item.devAlertLevel,
                    "devCpuRate": item.devCpuRate,
                    "devMemRate": item.devMemRate,
                    "devDiskRate": item.devDiskRate,
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
def update_server_data(request):
    """
    编辑服务器检测指标
    :param request:
    :return:
    """
    req_params = parse_json(request)
    server_data_id = req_params.get("id")
    sj_org_code = req_params.get("orgCode")  # 公安机关机构代码
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    ci_id = req_params.get("ciId")
    dev_online_state = req_params.get("devOnlineState")
    dev_response_time = req_params.get("devResponseTime")
    dev_alert_level = req_params.get("devAlertLevel")
    dev_cpu_rate = req_params.get("devCpuRate")
    dev_mem_rate = req_params.get("devMemRate")
    dev_disk_rate = req_params.get("devDiskRate")
    vd_res = is_data_validation_defeat('id', server_data_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        server_data = ServerData.objects.filter(id=server_data_id).first()
        if not server_data:
            return json_resp("编辑失败", None, 500)
        configs = [
            {"key": "orgCode", "value": sj_org_code, "v_type": "not_none"},
            {"key": "ciId", "value": ci_id, "v_type": "not_none"},
            {"key": "devOnlineState", "value": dev_online_state, "v_type": "not_none"},
            {"key": "devResponseTime", "value": dev_response_time, "v_type": "not_none"},
            {"key": "devAlertLevel", "value": dev_alert_level, "v_type": "not_in", "param": [3, 2, 1, 0]},
            {"key": "devCpuRate", "value": dev_cpu_rate, "v_type": "not_none"},
            {"key": "devMemRate", "value": dev_mem_rate, "v_type": "not_none"},
            {"key": "devDiskRate", "value": dev_disk_rate, "v_type": "not_none"},
            {"key": "isReported", "value": is_reported, "v_type": "not_in", "param": [1, 0]},
            {"key": "isDeleted", "value": is_deleted, "v_type": "not_in", "param": [1, 0]},
        ]
        res_obj = set_attr_by_data_valid(server_data, configs)
        if res_obj.get("msg") == "success":
            server_data = res_obj.get("obj")
        else:
            return json_resp(res_obj.get("msg"), None, 500)
        server_data.createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        server_data.updatedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        server_data.save()
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)
