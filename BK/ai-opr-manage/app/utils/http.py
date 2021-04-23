# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : http.py
@Time        : 2021/3/23 15:24
@Author      : yang xin
@Software    : PyCharm
@Description : 
"""
import json

import requests
from django.conf import settings


class HttpReq:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self):
        self.apiKey = settings.REPORT_APIKEY
        self.uri = settings.REPORT_HTTP_URL
        self.headers = {
            'Content-Type': 'application/json'
        }

    def req(self, path, data):
        res = {
            "success": True,
            "message": "操作成功！",
            "code": 200,
            "result": "上报成功1条,失败0条",
            "timestamp": '1601275719368'
        }
        # uri = self.uri + path + '?apikey=%s' % self.apiKey
        # res = requests.post(url=uri, data=json.dumps(data), headers=self.headers)
        # try:
        #     res = res.json()
        # except Exception as err:
        #     return False, '不是json'
        return True, res
