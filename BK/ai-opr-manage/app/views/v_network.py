# -*- coding: utf-8 -*-
from django.views.decorators.http import require_http_methods
from app.utils.util_req_resp import json_resp, parse_json
from app.utils.util_oracle_execute_sql import splice_sql, OracleExecuteSQL
from app.models import MachineRoom
from django.core.paginator import Paginator
from app.utils.util_data_valida import is_data_validation_defeat, set_attr_by_data_valid
from app.utils.util_page_number import get_actual_page


@require_http_methods(["POST"])
def fetch_network_run_list(request):
    """
    获取网络链路运行指标数据数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("ORG_CODE")
    link_state = req_params.get("LINK_STATE")
    # 执行sql语句
    table_name = "v_network_run_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "ORG_CODE", "value": sj_org_code, "condition": "="})
        if link_state in [10, 20]:
            keywords.append({"key": "LINK_STATE", "value": str(link_state), "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def fetch_network_perf_list(request):
    """
    获取网络设备监测指标数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("ORG_CODE")
    net_dev_online_state = req_params.get("NET_DEV_ONLINE_STATE")
    net_dev_alert_level = req_params.get("NET_DEV_ALERT_LEVEL")
    # 执行sql语句
    table_name = "v_network_perf_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "ORG_CODE", "value": sj_org_code, "condition": "="})
        if net_dev_online_state in [10, 20]:
            keywords.append({"key": "NET_DEV_ONLINE_STATE", "value": str(net_dev_online_state), "condition": "="})
        if net_dev_alert_level in [0, 1, 2, 3]:
            keywords.append({"key": "NET_DEV_ALERT_LEVEL", "value": str(net_dev_alert_level), "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def fetch_network_avg_list(request):
    """
    获取网络设备运行总体情况数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("ORG_CODE")
    # 执行sql语句
    table_name = "v_network_avg_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "ORG_CODE", "value": sj_org_code, "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def fetch_network_link_list(request):
    """
    获取网络骨干链路信息数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("ORG_CODE")
    # 执行sql语句
    table_name = "v_network_link_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "ORG_CODE", "value": sj_org_code, "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def fetch_hardware_resource_list(request):
    """
    获取硬件资源数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("SJ_ORG_CODE")
    sj_status = req_params.get("SJ_STATUS")
    sj_cl_network = req_params.get("SJ_CI_NETWORK")
    # 执行sql语句
    table_name = "v_hardware_resource_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "SJ_ORG_CODE", "value": sj_org_code+"", "condition": "="})
        if sj_status in [1, 2, 3, 4, 5, 6, 7, 8]:
            keywords.append({"key": "SJ_STATUS", "value": str(sj_status), "condition": "="})
        if sj_cl_network in [1, 2]:
            keywords.append({"key": "SJ_CI_NETWORK", "value": str(sj_cl_network), "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def fetch_room_situation_list(request):
    """
    获取机房情况数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    m_type = req_params.get("TYPE")
    if m_type == 1:  # 分局
       return branch(request)
    else:
        return police(request)


def branch(request):
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("SJ_ORG_CODE")
    sj_rm_name = req_params.get("SJ_RM_NAME")
    sj_is_th_mon = req_params.get("SJ_IS_TH_MON")
    sj_is_water_mon = req_params.get("SJ_IS_WATER_MON")
    sj_is_fire_mon = req_params.get("SJ_IS_FIRE_MON")

    # 执行sql语句
    table_name = "v_room_situation_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "SJ_ORG_CODE", "value": sj_org_code, "condition": "="})
        if sj_rm_name is not None and len(sj_rm_name.strip()) > 0:
            keywords.append({"key": "SJ_RM_NAME", "value": sj_rm_name + "", "condition": "like"})
        if sj_is_th_mon in [10, 20]:
            keywords.append({"key": "SJ_IS_TH_MON", "value": str(sj_is_th_mon), "condition": "="})
        if sj_is_water_mon in [10, 20]:
            keywords.append({"key": "SJ_IS_WATER_MON", "value": str(sj_is_water_mon), "condition": "="})
        if sj_is_fire_mon in [10, 20]:
            keywords.append({"key": "SJ_IS_FIRE_MON", "value": str(sj_is_fire_mon), "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


def police(request):
    """
    派出所
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("SJ_ORG_CODE")
    sj_rm_name = req_params.get("SJ_RM_NAME")
    sj_is_th_mon = req_params.get("SJ_IS_TH_MON")
    sj_is_water_mon = req_params.get("SJ_IS_WATER_MON")
    sj_is_fire_mon = req_params.get("SJ_IS_FIRE_MON")
    try:
        machine_room = MachineRoom.objects.filter(isDeleted=0).order_by("-id")
        vd_res = is_data_validation_defeat('SJ_ORG_CODE', sj_org_code, 'not_none')
        if not vd_res:
            machine_room = machine_room.filter(sJorgCode=sj_org_code)
        vd_res = is_data_validation_defeat('SJ_RM_NAME', sj_rm_name, 'not_none')
        if not vd_res:
            machine_room = machine_room.filter(sJrmName__contains=sj_rm_name)
        vd_res = is_data_validation_defeat('SJ_IS_TH_MON', sj_is_th_mon, 'not_none')
        if not vd_res:
            machine_room = machine_room.filter(sJisWatermon=sj_is_water_mon)
        vd_res = is_data_validation_defeat('SJ_IS_FIRE_MON', sj_is_fire_mon, 'not_none')
        if not vd_res:
            machine_room = machine_room.filter(sJisFiremon=sj_is_fire_mon)
        current_page = get_actual_page(len(machine_room), limit, current_page)
        paginator = Paginator(machine_room, limit)
        machine_room = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if machine_room:
            for item in machine_room:
                data_list.append({
                    "id": item.id,
                    "SJ_ORG_CODE": item.sJorgCode,
                    "SJ_RM_NAME": item.sJrmName,
                    "SJ_RM_CODE": item.sJrmCode,
                    "SJ_RM_POSITION": item.sJrmPosition,
                    "SJ_CAB_COUNT": item.sJcabCount,
                    "SJ_CAB_INSTALLED": item.sJcabInstalled,
                    "SJ_SD_TOTAL_CAPACITY": item.sJsdTotalCapacity,
                    "SJ_UPS_CAPACITY": item.sJupsCapacity,
                    "SJ_AIR_COUNT": item.sJairCount,
                    "SJ_IS_TH_MON": item.sJisTHmon,
                    "SJ_IS_WATER_MON": item.sJisWatermon,
                    "SJ_IS_FIRE_MON": item.sJisFiremon
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
def fetch_alarm_record_list(request):
    """
    获取基础故障告警数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("SJ_ORG_CODE")
    name = req_params.get("NAME")
    severity = req_params.get("SEVERITY")
    pro_status = req_params.get("PRO_STATUS")
    # 执行sql语句
    table_name = "v_alarm_record_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "SJ_ORG_CODE", "value": sj_org_code, "condition": "="})
        if name is not None and len(name.strip()) > 0:
            keywords.append({"key": "NAME", "value": name+"", "condition": "like"})
        if severity in [0, 1, 2]:
            keywords.append({"key": "SEVERITY", "value": str(severity), "condition": "="})
        if pro_status in [10, 20, 30]:
            keywords.append({"key": "PRO_STATUS", "value": str(pro_status), "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


@require_http_methods(["POST"])
def fetch_alarm_disposition_list(request):
    """
    获取故障处理工单数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    sj_org_code = req_params.get("SJ_ORG_CODE")
    one_solve = req_params.get("ONE_SOLVE")
    satisfaction = req_params.get("SATISFACTION")
    status = req_params.get("STATUS")
    # 执行sql语句
    table_name = "v_alarm_disposition_9"
    try:
        keywords = []
        if sj_org_code is not None and len(sj_org_code.strip()) > 0:
            keywords.append({"key": "SJ_ORG_CODE", "value": sj_org_code, "condition": "="})
        if one_solve in [10, 20, 30]:
            keywords.append({"key": "ONE_SOLVE", "value": str(one_solve), "condition": "="})
        if satisfaction in [10, 20, 30]:
            keywords.append({"key": "SATISFACTION", "value": str(satisfaction), "condition": "="})
        if status in [10, 20, 30, 40]:
            keywords.append({"key": "STATUS", "value": str(status), "condition": "="})
        sql, con_sql = splice_sql(table_name, limit, current_page, keywords=keywords)

        oracle_execute_sql = OracleExecuteSQL()

        object_list = oracle_execute_sql.fetchall_to_dict(sql)
        count = oracle_execute_sql.fetchone_to_dict(con_sql)
        data = {
            'count': count.get("COUNT", 0),
            'list': object_list,
            'current_page': current_page
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)