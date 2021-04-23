# -*- coding: utf-8 -*-

from check_system.models.models import CheckSystemOs
from check_system.models.tpl import Tpl

from blueking.component.shortcuts import get_client_by_user
from blueking.component.shortcuts import get_client_by_request


def by_user(username):
    """
    蓝鲸用户名获取client
    """
    return get_client_by_user(username)


def get_biz_os_tpl(request):
    # 获取对应的模板数据，OS数据，业务数据
    kwargs = {
        # 'bk_token': 'G6nuRLYKeKF2SKV2toXRNQVL9GWhOetUafkIMcsSSOM',
        "fields": [
            "bk_biz_id",
            "bk_biz_name"
        ],
    }

    client = get_client_by_request(request)
    res = client.cc.search_business(kwargs)

    # 业务模板
    bk_info_lists = {bk['bk_biz_id']: bk['bk_biz_name'] for bk in res['data']['info']}
    # 查询OS模板
    os_info_lists = {os.id: os.to_dict()['os_name'] for os in CheckSystemOs.objects.all()}
    # 查询指标模板
    tpl_info_lists = {tpl.id: tpl.to_dict_name()['tpl_name'] for tpl in Tpl.objects.all()}

    return bk_info_lists, os_info_lists, tpl_info_lists
