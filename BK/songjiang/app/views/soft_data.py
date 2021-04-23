# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import SoftData
from app.utils.util_page_number import get_actual_page
from app.utils.util_data_valida import is_data_validation_defeat, set_attr_by_data_valid
from app.utils.util_oracle_execute_sql import oracle_execute_sql


@require_http_methods(["POST"])
def fetch_soft_data_list(request):
    """
    获取软件实例运行指标数据
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
        soft_data_list = SoftData.objects.filter(isDeleted=0).order_by("-id")
        if update_time_range is not None and len(update_time_range):
            satm = update_time_range[0]
            edtm = update_time_range[1]
            soft_data_list = soft_data_list.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            soft_data_list = soft_data_list.filter(createdTime__range=(satm, edtm))
        vd_res = is_data_validation_defeat('id', server_data_id, 'not_none')
        if not vd_res:
            soft_data_list = soft_data_list.filter(id=server_data_id)
        vd_res = is_data_validation_defeat('sj_org_code', sj_org_code, 'not_none')
        if not vd_res:
            soft_data_list = soft_data_list.filter(orgCode=sj_org_code)
        vd_res = is_data_validation_defeat('sj_org_code', is_reported, 'not_none')
        if not vd_res:
            soft_data_list = soft_data_list.filter(isReported=is_reported)
        current_page = get_actual_page(len(soft_data_list), limit, current_page)
        paginator = Paginator(soft_data_list, limit)
        soft_data_list = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if soft_data_list:
            for item in soft_data_list:
                data_list.append({
                    "id": item.id,
                    "orgCode": item.orgCode,
                    "ciId": item.ciId,
                    "runningState": item.runningState,
                    "tcpState": item.tcpState,
                    "webResponseTime": item.webResponseTime,
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
        orcaletest()
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def update_soft_data(request):
    """
    编辑软件实例运行指标指标
    :param request:
    :return:
    """
    req_params = parse_json(request)
    server_data_id = req_params.get("id")
    sj_org_code = req_params.get("orgCode")  # 公安机关机构代码
    is_reported = req_params.get("isReported")
    is_deleted = req_params.get("isDeleted")
    ci_id = req_params.get("ciId")
    running_tate = req_params.get("runningState")
    tcp_tate = req_params.get("tcpState")
    web_response_time = req_params.get("webResponseTime")
    vd_res = is_data_validation_defeat('id', server_data_id, 'not_none')
    if vd_res:
        return json_resp(vd_res, None, 500)
    try:
        soft_data = SoftData.objects.filter(id=server_data_id).first()
        if not soft_data:
            return json_resp("编辑失败", None, 500)
        configs = [
            {"key": "orgCode", "value": sj_org_code, "v_type": "not_none"},
            {"key": "ciId", "value": ci_id, "v_type": "not_none"},
            {"key": "runningState", "value": running_tate, "v_type": "not_none"},
            {"key": "tcpState", "value": tcp_tate, "v_type": "not_none"},
            {"key": "webResponseTime", "value": web_response_time, "v_type": "not_none"},
            {"key": "isReported", "value": is_reported, "v_type": "not_in", "param": [1, 0]},
            {"key": "isDeleted", "value": is_deleted, "v_type": "not_in", "param": [1, 0]},
        ]
        res_obj = set_attr_by_data_valid(soft_data, configs)
        if res_obj.get("msg") == "success":
            soft_data = res_obj.get("obj")
        else:
            return json_resp(res_obj.get("msg"), None, 500)
        soft_data.createdTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        soft_data.updatedTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        soft_data.save()
        return json_resp("success")
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


def orcaletest():
    # 执行sql语句
    sql = "SELECT *  FROM \"v_network_run_9\""
    object_list = oracle_execute_sql.fetchall_to_dict(sql)
    print(object_list)


def fetchall_to_dict(sql, db='default', params=None, ):
    from django.db import connections
    """
    返回全部数据
    :param sql: sql语句
    :param params: sql语句参数
    :param db: Django数据库名
    :return: 例如：[{"id": id, "username": 'username', "first_name": 'first_name'}]
    """
    cursor = connections[db].cursor()
    cursor.execute(sql, params)
    desc = cursor.description
    object_list = [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    cursor.close()
    return object_list
