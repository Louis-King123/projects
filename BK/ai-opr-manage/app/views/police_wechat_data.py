# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import PoliceWechatData
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat


@require_http_methods(["POST"])
def fetch_police_wechat_data_list(request):
    """
    获取警务微信轻应用运行监控指标
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("orgCode")
    police_wechat_id = req_params.get("id")
    create_time_range = req_params.get("createTimeRange")
    update_time_range = req_params.get("updateTimeRange")
    app_name = req_params.get("appName")
    is_reported = req_params.get("isReported")
    try:
        police_wechat_data_list = PoliceWechatData.objects.filter(isDeleted=0).order_by("-id")
        if update_time_range is not None and len(update_time_range):
            satm = update_time_range[0]
            edtm = update_time_range[1]
            police_wechat_data_list = police_wechat_data_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            police_wechat_data_list = police_wechat_data_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('app_name', app_name, 'not_none')
        if not vd_res:
            police_wechat_data_list = police_wechat_data_list.filter(appName__icontains=app_name)
        vd_res = is_data_validation_defeat('id', police_wechat_id, 'not_none')
        if not vd_res:
            police_wechat_data_list = police_wechat_data_list.filter(id=police_wechat_id)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            police_wechat_data_list = police_wechat_data_list.filter(orgCode=sj_org_code)
        vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_none')
        if not vd_res:
            police_wechat_data_list = police_wechat_data_list.filter(isReported=is_reported)
        current_page = get_actual_page(len(police_wechat_data_list), limit, current_page)
        paginator = Paginator(police_wechat_data_list, limit)
        police_wechat_data_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if police_wechat_data_list:
            for item in police_wechat_data_list:
                data_list.append({
                    "id": item.id,
                    "orgCode": item.orgCode,
                    "agentid": item.agentid,
                    "appName": item.appName,
                    "checkTime": item.checkTime,
                    "result": item.result,
                    "expdesc": item.expdesc,
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
def update_police_wechat_data(request):
    """
    编辑警务微信轻应用运行监控指标
    :param request:
    :return:
    """
    req_params = parse_json(request)
    police_wechat_id = req_params.get("id")
    sj_org_code = req_params.get("orgCode")  # 公安机关机构代码
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    agent_id = req_params.get("agentid")
    app_name = req_params.get("appName")
    check_time = req_params.get("checkTime")
    result = req_params.get("result")
    expdesc = req_params.get("expdesc")
    vd_res = is_data_validation_defeat('id', police_wechat_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        police_wechat_data = PoliceWechatData.objects.filter(id=police_wechat_id).first()
        if not police_wechat_data:
            return json_resp("编辑失败", None, 500)
        if sj_org_code is not None:
            police_wechat_data.orgCode = sj_org_code
        if agent_id is not None:
            police_wechat_data.agentid = agent_id
        if app_name is not None:
            police_wechat_data.appName = app_name
        if check_time is not None:
            police_wechat_data.checkTime = check_time
        if result is not None:
            vd_res = is_data_validation_defeat('result', result, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            police_wechat_data.result = result
        if expdesc is not None:
            police_wechat_data.expdesc = expdesc
        if is_reported is not None:
            vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            police_wechat_data.isReported = is_reported
        if is_deleted is not None:
            vd_res = is_data_validation_defeat('is_deleted', is_deleted, 'not_in', [1, 0])
            if vd_res:
                return json_resp(vd_res, None, 500)
            police_wechat_data.isDeleted = is_reported
        police_wechat_data.createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        police_wechat_data.updatedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        police_wechat_data.save()
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)
