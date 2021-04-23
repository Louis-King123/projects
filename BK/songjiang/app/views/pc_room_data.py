# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import PcRoomData
from app.utils.util_time import get_str_from_datetime
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat


def fetch_pc_room_data_list(request):
    """
    获取机房环境运行指标数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("orgCode")
    pc_room_id = req_params.get("id")
    create_time_range = req_params.get("createTimeRange")
    update_time_range = req_params.get("updateTimeRange")
    is_reported = req_params.get("isReported")
    try:
        pc_room_data_list = PcRoomData.objects.filter(isDeleted=0).order_by("-id")
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            pc_room_data_list = pc_room_data_list.filter(orgCode=sj_org_code)
        vd_res = is_data_validation_defeat('id', pc_room_id, 'not_none')
        if not vd_res:
            pc_room_data_list = pc_room_data_list.filter(id=pc_room_id)
        if update_time_range is not None and len(update_time_range) == 2:
            satm = update_time_range[0]
            edtm = update_time_range[1]
            pc_room_data_list = pc_room_data_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            pc_room_data_list = pc_room_data_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_none')
        if not vd_res:
            pc_room_data_list = pc_room_data_list.filter(isReported=is_reported)
        current_page = get_actual_page(len(pc_room_data_list), limit, current_page)
        paginator = Paginator(pc_room_data_list, limit)
        pc_room_data_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if pc_room_data_list:
            for item in pc_room_data_list:
                data_list.append({
                    "id": item.id,
                    "orgCode": item.orgCode,
                    "rmCode": item.rmCode,
                    "envHealthValue": item.envHealthValue,
                    "powerHealthValue": item.powerHealthValue,
                    "electrRealPower": item.electrRealPower,
                    "upsRealPower": item.upsRealPower,
                    "roomAverTemp": item.roomAverTemp,
                    "roomAverHum": item.roomAverHum,
                    "waterLeakStatus": item.waterLeakStatus,
                    "fireStatus": item.fireStatus,
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
def update_pc_room_data(request):
    """
    编辑机房环境运行指标
    :param request:
    :return:
    """
    req_params = parse_json(request)
    pc_room_id = req_params.get("id")
    sj_org_code = req_params.get("orgCode")  # 公安机关机构代码
    rm_code = req_params.get("rmCode")
    env_health_value = req_params.get("envHealthValue")
    power_ealth_value = req_params.get("powerHealthValue")
    electr_real_power = req_params.get("electrRealPower")
    ups_real_power = req_params.get("upsRealPower")
    room_aver_temp = req_params.get("roomAverTemp")
    room_aver_hum = req_params.get("roomAverHum")
    water_leak_status = req_params.get("waterLeakStatus")
    fire_status = req_params.get("fireStatus")
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    vd_res = is_data_validation_defeat('id', pc_room_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        pc_room_data = PcRoomData.objects.filter(id=pc_room_id).first()
        if not pc_room_data:
            return json_resp("编辑失败", None, 500)
        if sj_org_code is not None:
            pc_room_data.orgCode = sj_org_code
        if rm_code is not None:
            pc_room_data.rmCode =rm_code
        if env_health_value is not None:
            pc_room_data.envHealthValue = env_health_value
        if power_ealth_value is not None:
            pc_room_data.powerHealthValue = power_ealth_value
        if electr_real_power is not None:
            pc_room_data.electrRealPower = electr_real_power
        if ups_real_power is not None:
            pc_room_data.upsRealPower = ups_real_power
        if room_aver_temp is not None:
            pc_room_data.roomAverTemp = room_aver_temp
        if water_leak_status is not None:
            pc_room_data.waterLeakStatus = water_leak_status
        if room_aver_hum is not None:
            pc_room_data.roomAverHum = room_aver_hum
        if fire_status is not None:
            pc_room_data.fireStatus = fire_status
        if is_reported is not None:
            vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            pc_room_data.isReported = is_reported
        if is_deleted is not None:
            vd_res = is_data_validation_defeat('is_deleted', is_deleted, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            pc_room_data.isDeleted = is_reported
        pc_room_data.createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pc_room_data.updatedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        pc_room_data.save()
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def delete_pc_room_data(request):
    """
    批量删除机房环境运行指标
    :param request:
    :return:
    """
    req_params = parse_json(request)
    ids = req_params.get("ids")
    try:
        vd_res = is_data_validation_defeat('ids', ids, 'is_list')
        if vd_res:
            return json_resp(vd_res, None, 500)
        PcRoomData.objects.filter(id__in=ids).update(isDeleted=1)
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)



