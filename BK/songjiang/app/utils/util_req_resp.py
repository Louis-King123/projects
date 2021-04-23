# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse


def parse_json(request):
    req_param = {}
    try:
        if request.body:
            req_param = json.loads(request.body)
    finally:
        return req_param


def json_resp(msg='', data=None, code=200):
    return JsonResponse({
        'message': msg,
        'data': data,
        'code': code
    })
