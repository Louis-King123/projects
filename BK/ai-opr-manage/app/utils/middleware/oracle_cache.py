# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : oracle_cache.py
@Time        : 2021/4/1 12:54
@Author      : yang xin
@Software    : PyCharm
@Description : 
"""
import json

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class OracleCacheMiddleware(MiddlewareMixin):
    """
    缓存oracle的数据
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oracle_path_list = settings.ORACLE_PATH_LIST
        self.oracle_cache_timeout = settings.ORACLE_CACHE_TIMEOUT
        # 接口作为key
        self.key = None
        self.leap = False

    def process_request(self, request):
        self.key = request.path
        if self.key in self.oracle_path_list:
            val = cache.get(self.key)
            if val:
                self.leap = True
                return JsonResponse(val)

    def process_view(self, request, view, args, kwargs):
        pass

    def process_response(self, request, response):
        # 是否从oracle取数据
        if self.key not in self.oracle_path_list:
            return response

        # 是不是从缓存取数据
        if self.leap:
            self.leap = False
            return response

        # 缓存oracle数据
        res_data = response._container[0].decode()
        res_data = json.loads(res_data)
        if res_data.get('code') == 200:
            cache.set(self.key, res_data, self.oracle_cache_timeout)
            return response
        return response