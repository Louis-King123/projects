# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import FaultAlert
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat, batch_verification


@require_http_methods(["POST"])
def fetch_fault_alert_list(request):
    """
    获取故障告警数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("orgCode")
    cloud_serve_type_id = req_params.get("id")
    create_time_range = req_params.get("createTimeRange")
    update_time_range = req_params.get("updateTimeRange")
    is_reported = req_params.get("isReported")
    severity = req_params.get("severity")
    try:
        cloud_serve_type_list = FaultAlert.objects.filter(isDeleted=0).order_by("-id")
        if update_time_range is not None and len(update_time_range) == 2:
            satm = update_time_range[0]
            edtm = update_time_range[1]
            cloud_serve_type_list = cloud_serve_type_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            cloud_serve_type_list = cloud_serve_type_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('id', cloud_serve_type_id, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(id=cloud_serve_type_id)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(orgCode=sj_org_code)
        vd_res = is_data_validation_defeat('is_reported', is_reported, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(isReported=is_reported)
        vd_res = is_data_validation_defeat('severity', severity, 'not_none')
        if not vd_res:
            cloud_serve_type_list = cloud_serve_type_list.filter(severity=severity)
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
                    "orgCode": item.orgCode,
                    "alertId": item.alertId,
                    "name": item.name,
                    "severity": item.severity,
                    "description": item.description,
                    "entityName": item.entityName,
                    "entityAddr": item.entityAddr,
                    "firstTime": item.firstTime,
                    "lastTime": item.lastTime,
                    "properties": item.properties,
                    "ciId": item.ciId,
                    "proStatus": item.proStatus,
                    "orderNo": item.orderNo,
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