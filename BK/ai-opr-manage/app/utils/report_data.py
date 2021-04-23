# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : report_data.py
@Time        : 2021/3/24 19:19
@Author      : yang xin
@Software    : PyCharm
@Description : 
"""
from datetime import datetime

from django.forms import model_to_dict

from app.models import ReportLog


# 上报日志
def report_log(**kwargs):
    ReportLog.objects.create(**kwargs)


# 上报数据序列化
def to_dict(querysets, entity, tup=('id', 'isReported', 'isDeleted', 'createdTime', 'updatedTime'), class_code=None):
    lst = []
    for queryset in querysets:
        dic = model_to_dict(queryset, exclude=tup)
        if class_code:
            dic['classCode'] = class_code
        for key, value in dic.items():
            if isinstance(value, datetime):
                dic[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        lst.append(dic)
    if not lst:
        fields = entity._meta.fields
        dic = {field.name: str(0) for field in fields if field.name not in tup}
        if class_code:
            dic['classCode'] = class_code
        lst.append(dic)
    print(lst)
    return lst

