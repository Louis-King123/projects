# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Avg
from app.utils.util_req_resp import json_resp, parse_json
from app.models import ServerDataAll
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat, set_attr_by_data_valid


@require_http_methods(["POST"])
def fetch_server_data_all_list(request):
    """
    获取服务器监测总体情况数据
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
    try:
        server_data_all_list = ServerDataAll.objects.filter(isDeleted=0).order_by("-id")
        if update_time_range is not None and len(update_time_range):
            satm = update_time_range[0]
            edtm = update_time_range[1]
            server_data_all_list = server_data_all_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            server_data_all_list = server_data_all_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('id', server_data_id, 'not_none')
        if not vd_res:
            server_data_all_list = server_data_all_list.filter(id=server_data_id)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            server_data_all_list = server_data_all_list.filter(orgCode=sj_org_code)
        vd_res = is_data_validation_defeat('isReported', is_reported, 'not_none')
        if not vd_res:
            server_data_all_list = server_data_all_list.filter(isReported=is_reported)
        current_page = get_actual_page(len(server_data_all_list), limit, current_page)
        paginator = Paginator(server_data_all_list, limit)
        server_data_all_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if server_data_all_list:
            for item in server_data_all_list:
                data_list.append({
                    "id": item.id,
                    "orgCode": item.orgCode,
                    "devHealthValue": item.devHealthValue,
                    "devOnlineRate": item.devOnlineRate,
                    "devAverCpuRate": item.devAverCpuRate,
                    "devAverMemRate": item.devAverMemRate,
                    "devAverDiskRate": item.devAverDiskRate,
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
def update_server_data_all(request):
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
    dev_health_value = req_params.get("devHealthValue")
    dev_online_rate = req_params.get("devOnlineRate")
    dev_aver_cpu_rate = req_params.get("devAverCpuRate")
    dev_aver_mem_rate = req_params.get("devAverMemRate")
    dev_aver_disk_rate = req_params.get("devAverDiskRate")
    vd_res = is_data_validation_defeat('id', server_data_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        server_data_all = ServerDataAll.objects.filter(id=server_data_id).first()
        if not server_data_all:
            return json_resp("编辑失败", None, 500)
        configs = [
            {"key": "orgCode", "value": sj_org_code, "v_type": "not_none"},
            {"key": "devHealthValue", "value": dev_health_value, "v_type": "not_none"},
            {"key": "devOnlineRate", "value": dev_online_rate, "v_type": "not_none"},
            {"key": "devAverCpuRate", "value": dev_aver_cpu_rate, "v_type": "not_none"},
            {"key": "devAverMemRate", "value": dev_aver_mem_rate, "v_type": "not_none"},
            {"key": "devAverDiskRate", "value": dev_aver_disk_rate, "v_type": "not_none"},
            {"key": "isReported", "value": is_reported, "v_type": "not_in", "param": [1, 0]},
            {"key": "isDeleted", "value": is_deleted, "v_type": "not_in", "param": [1, 0]},
        ]
        res_obj = set_attr_by_data_valid(server_data_all, configs)
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


def get_avg_indicators(request):
    """
        获取服务器监测总体情况各项平均指标
        :param request:
        :return:
        """
    try:
        server_data_all = ServerDataAll.objects.filter(isDeleted=0).aggregate(
            devOnlineRate=Avg('devOnlineRate'),
            devAverCpuRate=Avg('devAverCpuRate'),
            devAverMemRate=Avg('devAverMemRate'),
            devAverDiskRate=Avg('devAverDiskRate')
        )
        # for item in server_data_all.keys():

        return json_resp("success", data=server_data_all)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)



