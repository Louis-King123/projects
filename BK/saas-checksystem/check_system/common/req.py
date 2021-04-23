# -*- coding: utf-8 -*-

import json


def req_body_to_json(request):
    """
    获取request body转成json
    """
    body = request.body.decode()
    return json.loads(body)
