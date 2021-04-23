# -*- coding: utf-8 -*-
import time
from itertools import groupby
from operator import itemgetter

from check_system.models import Quota
from check_system.models.check_class import CheckSystemClass


def quota_class(quotas, tpl_quotas=list()):
    """
    根据指标所属类 返回可视化列表
    @param quotas: 指标列表
    """
    quota_id_list = list()
    class_quota_dict = dict()
    # 查询所有关联指标
    tpl_quota_dict = {str(tpl_quota.quota_id): tpl_quota for tpl_quota in tpl_quotas}

    # 通过key:[value1,value2]形式存储指标
    for quota in quotas:
        data = quota.to_dict_onshow()
        if tpl_quota_dict:
            data["quota_threshold"] = tpl_quota_dict[str(quota.id)].quota_threshold
        if quota.quota_class in class_quota_dict:
            class_quota_dict[quota.quota_class].append(data)
        else:
            class_quota_dict[quota.quota_class] = [data]

        # 将classID 存入列表
        quota_id_list.append(quota.quota_class)

    quota_id_list = list(set(quota_id_list))
    # 根据多个classID 查询结果
    system_class = CheckSystemClass.objects.filter(id__in=quota_id_list).order_by('sort')
    data = [{"id": str(class_obj.id), "class_name": class_obj.class_name, "children": class_quota_dict[str(class_obj.id)]} for class_obj in system_class]

    return data


def tpl_quotas(quotas):
    """
    根据指标中间表 查询指标名称及参考值
    @quotas:指标中间表
    """
    # 查询所有关联指标
    tpl_quota_dict = {str(quota['id']): quota for quota in quotas}

    # 查询所有关联指标
    quotas = Quota.objects.filter(id__in=[quota['id'] for quota in quotas]).all()

    for quota in quotas:
        tpl_quota_dict[str(quota.id)]['quota_name'] = quota.quota_name
        tpl_quota_dict[str(quota.id)].pop('id')

    return [value for value in tpl_quota_dict.values()]
