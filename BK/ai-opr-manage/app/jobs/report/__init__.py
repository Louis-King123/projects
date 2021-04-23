# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : __init__.py.py
@Time        : 2021/3/23 15:12
@Author      : yang xin
@Software    : PyCharm
@Description : 
"""
import re

from django.utils import timezone


def just_response(res, police_wechat=None):
    """
    判断数据上报返回状态
    :param res:
    :param police_wechat: 警务微信轻应用类别
    :return:
    """
    cmp = '上报成功'
    desc = res.get('result')
    if police_wechat:
        if res.get('code') == 200 and res.get('success'):
            return True
        return False
    if desc:
        result = re.findall(r'[上报成功]', desc)
        result = ''.join(result)
        if cmp == result:
            return True
        if cmp in desc:
            return True
    return False


# 日志数据
def log_data(report_type, request_data, result_data):
    return {
            'reportType': report_type,
            'requestData': request_data,
            'resultData': result_data,
            'createdTime': timezone.now(),
            'updatedTime': timezone.now(),
        }