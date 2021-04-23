# !/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@File        : forms.py
@Time        : 2021/3/27 17:33
@Author      : yang xin
@Software    : PyCharm
@Description : 
"""

from django import forms


class PageForm(forms.Form):
    keyword = forms.CharField(max_length=20, required=False, label='搜索')
    page = forms.IntegerField(min_value=1, label='页码')
    pageSize = forms.IntegerField(min_value=1, label='条数')