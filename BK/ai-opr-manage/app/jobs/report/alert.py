# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : alert.py
@Time        : 2021/3/27 11:40
@Author      : yang xin
@Software    : PyCharm
@Description : 故障告警
"""
import json
import time

from app.jobs.report import log_data, just_response
from app.models import FaultAlert
from app.utils.http import HttpReq
from django.conf import settings

from app.utils.report_data import to_dict, report_log


class AlertData:
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
        # 请求路径
        self.uri_path = settings.PUSH_ALERT

    def report_logic(self, entity):
        """
        上报逻辑
        :param entity:
        :return:
        """
        self.i += 1
        querysets = entity.objects.filter(isDeleted=0, isReported=0)
        report_data = to_dict(querysets, entity)
        status, res = self.http.req(self.uri_path, report_data)
        result_data = json.dumps(res) if status else res
        report_log(**log_data(3, json.dumps(report_data), result_data))
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
            self.report_logic(entity)
        else:
            self.i = 1

    def fault_alert(self):
        self.report_logic(FaultAlert)


# 故障告警数据上报
def alert_work():
    alert_obj = AlertData()
    # alert_obj.fault_alert()
