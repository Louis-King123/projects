# -*- coding: utf-8 -*-
"""
日志读取工具
"""

import re


def get_nums_from_line(line):
    """
    从字符串中读取纯数字，返回数字字符串list ["1", "2"]
    @param line: 字符串
    """
    return re.findall(r"\b\d+\b", line)


def get_none_space_str_from_line(line):
    """
    从字符串中读取非空字符串，返回数字字符串list ["aa", "2"]
    @param line: 字符串
    """
    return re.findall(r"\b\w+\b", line)


def get_dict_from_log_kv(log, key_index=0, val_index=1):
    """
    从日志字符串中读取出dict

    参数
    log
        420 ESTABLISHED
        127 TIME_WAIT
         69 LISTEN
          1 CLOSE_WAIT
    key_index 1
    val_index 0

    返回
    {
        "ESTABLISHED": "420",
        "TIME_WAIT": "127",
        "LISTEN": "69",
        "CLOSE_WAIT": "1"
    }

    @param log: 日志字符串
    @param key_index: key值的位置
    @param val_index: val值的位置
    """
    result = {}
    for line in log.split("\n"):
        str_list = get_none_space_str_from_line(line)

        if len(str_list) == 2:
            val = str_list[val_index]
            key = str_list[key_index]

            result[key] = val

    return result


def get_dict_from_line_by_given_dict(line, d):
    """
    从日志字符串中读取出dict 使用指定的dict

    日志类型
    Swap:       8122196      137728     7984468

    参数
    {
        "name": 0,
        "total": 1,
        "used": 2,
        "free": 3
    }

    返回
    {
        "name": "Swap",
        "total": "8122196",
        "used": "137728",
        "free": "7984468"
    }

    @param line: 日志字符串
    @param d: dict 内容是键值对应的参数位置
    """
    str_list = get_none_space_str_from_line(line)

    if len(str_list) > 0:
        temp = {}
        for (key, idx) in d.items():
            temp[key] = str_list[idx] if len(str_list) > idx else ""

        return temp

    return {}


def get_dict_from_log_by_given_dict(log, d):
    """
    从日志字符串中读取出dict 使用指定的dict

    日志类型
    Swap:       8122196      137728     7984468

    参数
    {
        "name": 0,
        "total": 1,
        "used": 2,
        "free": 3
    }

    返回
    [{
        "name": "Swap",
        "total": "8122196",
        "used": "137728",
        "free": "7984468"
    }]

    @param log: 日志字符串
    @param d: dict 内容是键值对应的参数位置
    """
    result = []
    for line in log.split("\n"):
        result.append(get_dict_from_line_by_given_dict(line, d))

    return result
