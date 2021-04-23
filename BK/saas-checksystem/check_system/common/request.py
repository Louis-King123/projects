# -*- coding: utf-8 -*-
from django.http import JsonResponse, request


class Request:

    def __init__(self, request):
        pass

    @classmethod
    def succFcun(cls, msg='操作成功', data=[]):
        return JsonResponse({
            "result": True,
            "message": msg,
            "code": 0,
            "data": data
        })

    @classmethod
    def errorFcun(cls, msg='操作失败', data=[]):
        return JsonResponse({
            "result": False,
            'code': 1,
            'message': msg,
            'data': data
        })
