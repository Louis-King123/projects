# -*- coding: utf-8 -*-
import time
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Sum
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import PoliceWechatData, FaultAlert, CloudDataAll, SoftData, BaseSoftData
from app.utils.util_oracle_execute_sql import get_table_name, OracleExecuteSQL
from django.conf import settings


@require_http_methods(["POST"])
def get_data_source(request):
    """
    获取数据来源
    """
    try:
        # 微信轻应用数
        wechat_data = PoliceWechatData.objects.filter(isDeleted=0).values('appName').annotate(count=Count("id"))

        # 动环告警未处理数据
        alert_non_process = FaultAlert.objects.filter(proStatus=10, isDeleted=0).aggregate(count=Count("id"))
        # 故障告警未处理数据
        sql = "SELECT COUNT(1) as count FROM  " + get_table_name('v_alarm_record_9') + " WHERE PRO_STATUS='10'"

        oracle_execute_sql = OracleExecuteSQL()

        alarm_record = oracle_execute_sql.fetchone_to_dict(sql)
        # 云上服务类型数，云上应用数
        ser_app_list = CloudDataAll.objects.filter(isDeleted=0)
        ser_app_count = get_ser_app_count(ser_app_list)
        ser_type_count = CloudDataAll.objects.filter(isDeleted=0).values('sJcloudBrand').annotate(count=Count("id"))
        #  软件实例数
        soft_data = SoftData.objects.filter(isDeleted=0).aggregate(count=Count("id"))
        #  基础软件实例数
        base_soft_data = BaseSoftData.objects.filter(isDeleted=0).values('sJsoftName').annotate(count=Count("id"))
        #  机房数
        sql = "SELECT SJ_RM_CODE  FROM  " + get_table_name('v_room_situation_9') + "ORDER BY 'SJ_RM_CODE'"
        room_data = oracle_execute_sql.fetchall_to_dict(sql)
        #  工单未解决
        sql = "SELECT COUNT(1) as count FROM " + get_table_name('v_alarm_disposition_9') + " WHERE ONE_SOLVE='30'"
        work_order = oracle_execute_sql.fetchone_to_dict(sql)
        #  硬件资源
        sql = "SELECT SJ_CI_ID FROM  " + get_table_name('v_hardware_resource_9') + "ORDER BY 'SJ_CI_ID'"
        hardware_resources = oracle_execute_sql.fetchall_to_dict(sql)
        #  获取网络设备指标
        sql = "SELECT AVG(NET_DEV_CPU_RATE) as NET_DEV_CPU_RATE, AVG(NET_DEV_MEM_RATE) AS NET_DEV_MEM_RATE FROM  " + get_table_name(
            'v_network_perf_9')
        network_perf = oracle_execute_sql.fetchone_to_dict(sql)
        #  获取网络设备在线率
        sql = "SELECT COUNT(1) as count FROM  " + get_table_name(
            'v_network_perf_9') + " WHERE NET_DEV_ONLINE_STATE = '10'"
        on_line = oracle_execute_sql.fetchone_to_dict(sql)
        sql = "SELECT COUNT(1) as count FROM  " + get_table_name('v_network_perf_9')
        count = oracle_execute_sql.fetchone_to_dict(sql)
        on_line_rate = on_line.get("COUNT") / count.get("COUNT") * 100
        data = {
            "data_source": {
                "wechat_data": len(wechat_data),  # 微信轻应用数
                "ser_app_count": ser_app_count,  # 云上应用数
                "ser_type_count": len(ser_type_count),  # 云上服务类型数
                "soft_data": soft_data.get("count"),  # 软件实例数
                "base_soft_data": len(base_soft_data)
            },
            "top_data": {
                "room_data": len(room_data),
                "alert_non_process": alert_non_process.get("count") + alarm_record.get("COUNT"),  # 告警未处理数据
                "work_order_not_process": work_order.get("COUNT"),  # 工单未处理数
                "hardware_resources": len(hardware_resources)  # 硬件资源
            },
            "network_perf": {
                "net_dev_cpu_rate": network_perf.get("NET_DEV_CPU_RATE"),
                "net_dev_men_rate": network_perf.get("NET_DEV_MEM_RATE"),
                "on_line_rate": on_line_rate
            }
        }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)


def get_ser_app_count(ser_app_list):
    ser_app_temp = []
    count = 0
    for item in ser_app_list:
        if len(ser_app_temp) == 0:
            ser_app_temp.append(item)
            count = item.sJcloudAppCount
        for ser_app_item in ser_app_temp:
            if ser_app_item.sJcloudServCount != item.sJcloudServCount:
                ser_app_temp.append(item)
                count += item.sJcloudAppCount
    return count
