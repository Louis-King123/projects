# -*- coding: utf-8 -*-

from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request

# 测试的业务ID
BK_BIZ_ID = 4


def fetch_host_list(request):
    """
    查询业务列表
    """
    client = get_client_by_request(request)

    host_list = []
    res = client.cc.search_host({"bk_biz_id": BK_BIZ_ID})
    if res["result"]:
        host_list = [h["host"] for h in res["data"]["info"]]

    return JsonResponse({
        "result": True,
        "data": host_list,
        "message": ""
    })


def search_host_by_biz(request):
    """
    查询主机根据业务
    """
    res = {'code': 0, 'message': '操作成功', 'data': []}
    client = get_client_by_request(request)
    where = {
        "page": {
            "start": 0,
            "limit": 200
        }
    }
    result = client.cc.search_business(where)

    if not result.get('result', False):
        return JsonResponse(res, safe=False)

    biz = {}
    for val in result['data']['info']:
        temp = gethosts(client, val['bk_biz_id'])
        if len(temp) > 0:
            biz[val['bk_biz_id']] = {
                'id': val['bk_biz_id'],
                'name': val['bk_biz_name'],
                'children': temp
            }

    res['data'] = biz

    return JsonResponse(res, safe=False)


def gethosts(client, biz_id):
    """
    获取host
    """
    where = {
        "page": {
            "start": 0,
            "limit": 10,
            "sort": "bk_host_id"
        },
        "bk_biz_id": biz_id
    }

    # result = client.cc.list_biz_hosts(where)
    # if not result.get('result', False):
    #     return []
    #
    # hosts = []
    # for val in result['data']['info']:
    #     hosts.append({
    #         'id': val['bk_host_innerip'],
    #         'name': 'ip:' + val['bk_host_innerip'] + '-name:' + val['bk_host_name'],
    #     })

    result = client.cc.search_host(where)
    if not result.get('result', False):
        return []

    hosts = []
    for val in result['data']['info']:
        hosts.append({
            'id': val['host']['bk_host_innerip'],
            'name': 'ip:' + val['host']['bk_host_innerip'] + '-name:' + val['host']['bk_host_name'],
        })

    return hosts
