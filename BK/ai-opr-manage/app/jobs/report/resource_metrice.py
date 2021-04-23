# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : resource_metrice.py
@Time        : 2021/3/23 15:17
@Author      : yang xin
@Software    : PyCharm
@Description : 资源运行状态与关键性能指标数据
"""
import json
import time
import threading

from app.jobs.report import log_data, just_response
from app.models import PcRoomData, ServerDataAll, ServerData, SoftData, PoliceWechatData
from app.utils.http import HttpReq
from django.conf import settings

from app.utils.report_data import report_log, to_dict


class ResouceMetricData:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self):
        # request
        self.http = HttpReq()
        # 上报计数
        self.i = 1

    # 警务微信上报逻辑
    def police_wechat_logic(self, report_data):
        i = 0
        uri_path = settings.PUSH_WECHAT_MONITOR
        while i < 50:
            status, res = self.http.req(uri_path, report_data)
            result_data = json.dumps(res) if status else res
            report_log(**log_data(2, json.dumps(report_data), result_data))
            if status:
                if just_response(res, 'police'):
                    break
            i += 1
            time.sleep(3)

    def report_logic(self, uri_path, entity):
        """
        上报逻辑
        :param uri_path:
        :param entity: model 实体
        :return:
        """
        self.i += 1
        querysets = entity.objects.filter(isDeleted=0, isReported=0)
        report_data = to_dict(querysets, entity)
        status, res = self.http.req(uri_path, report_data)
        result_data = json.dumps(res) if status else res
        report_log(**log_data(2, json.dumps(report_data), result_data))
        # 判断返回的数据是否是json
        if status:
            # 根据result判断是否成功 result是一串文字, 应根据code 或 success
            if just_response(res):
                querysets.update(isReported=1)
                self.i = 1
                return
        # 失败重新上报 最大50次
        if self.i <= 50:
            time.sleep(3)
            self.report_logic(uri_path, entity)
        else:
            self.i = 1

    # 机房环境运行指标数据
    def pc_room_metric(self):
        uri_path = settings.PUSH_ROOM
        self.report_logic(uri_path, PcRoomData)

    # 服务器监测总体情况
    def serve_all_metric(self):
        uri_path = settings.PUSH_SERVE
        self.report_logic(uri_path, ServerDataAll)

    # 服务器监测指标
    def serve_detail_metric(self):
        uri_path = settings.PUSH_SERVE_METRIC
        self.report_logic(uri_path, ServerData)

    # 软件实例运行指标
    def software_metric(self):
        uri_path = settings.PUSH_SOFTWARE
        self.report_logic(uri_path, SoftData)

    # 警务微信轻应用运行监控指标
    def police_wechat_metric(self):
        querysets = PoliceWechatData.objects.filter(isDeleted=0, isReported=0)
        report_data = to_dict(querysets, PoliceWechatData)
        thread_list = []
        for dic in report_data:
            thread_res = threading.Thread(target=self.police_wechat_logic, args=(dic,))
            thread_list.append(thread_res)
        for th in thread_list:
            th.start()
        for th in thread_list:
            th.join()
        querysets.update(isReported=1)


# 启动资源指标数据上报
def resouce_metric_work():
    resouce_metric_obj = ResouceMetricData()
    resouce_metric_obj.pc_room_metric()
    resouce_metric_obj.serve_all_metric()
    resouce_metric_obj.serve_detail_metric()
    resouce_metric_obj.software_metric()
    resouce_metric_obj.police_wechat_metric()