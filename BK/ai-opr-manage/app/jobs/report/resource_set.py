# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : resource_set.py
@Time        : 2021/3/23 15:16
@Author      : yang xin
@Software    : PyCharm
@Description : 资源配置数据
"""
import json
import time

from app.jobs.report import just_response, log_data
from app.models import BaseSoftData, CloudDataAll, CloudServeType, MachineRoom
from django.conf import settings

from app.utils.http import HttpReq
from app.utils.report_data import to_dict, report_log


class ResouceSetData:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self):
        # 机房情况
        self.jfjsqk = 'jfjsqk'
        # 硬件资源
        self.itLryjzy = 'itLryjzy'
        # 虚拟资源
        self.sJxnzy = 'sJxnzy'
        # 虚拟化平台
        self.sJxnhptjskq = 'sJxnhptjskq'
        # 云平台总体建设情况
        self.sJyptztjsqk = 'sJyptztjsqk'
        # 云平台分服务类型建设情况
        self.sJyptffwlxjsqk = 'sJyptffwlxjsqk'
        # 基础软件实例
        self.sJjcrjsl = 'sJjcrjsl'
        # 网络骨干链路信息
        self.sJwlqgllxx = 'sJwlqgllxx'
        # request
        self.http = HttpReq()
        # 上报计数
        self.i = 1
        # 请求路径
        self.uri_path = settings.RESOURCE_PUSH

    def report_logic(self, entity, class_code):
        """
        上报逻辑
        :param entity:
        :param class_code:  类型编码
        :return:
        """
        self.i += 1
        querysets = entity.objects.filter(isDeleted=0, isReported=0)
        report_data = to_dict(querysets, entity, class_code=class_code)
        status, res = self.http.req(self.uri_path, report_data)
        result_data = json.dumps(res) if status else res
        report_log(**log_data(1, json.dumps(report_data), result_data))
        # 判断返回的数据是否是json
        if status:
            # 根据result判断是否成功 result是一串文字, 应根据code 或 success
            if just_response(res):
                querysets.update(isReported=1)
                self.i = 1
                return
        # 失败重新上报 最大50次
        if self.i <= 50:
            print('调用了')
            time.sleep(3)
            self.report_logic(entity, class_code)
        else:
            self.i = 1

    # 机房情况
    def machine_room(self):
        self.report_logic(MachineRoom, self.jfjsqk)

    # 基础软件实例
    def base_soft_data(self):
        self.report_logic(BaseSoftData, self.sJjcrjsl)

    # 云平台总体建设
    def cloud_data_all(self):
        self.report_logic(CloudDataAll, self.sJyptztjsqk)

    # 云平台分服务类型建设
    def cloud_serve_type(self):
        self.report_logic(CloudServeType, self.sJyptffwlxjsqk)


# 启动资源配置数据上报
def resouce_set_work():
    resouce_set_obj = ResouceSetData()
    # resouce_set_obj.machine_room()
    # resouce_set_obj.base_soft_data()
    # resouce_set_obj.cloud_data_all()
    # resouce_set_obj.cloud_serve_type()

