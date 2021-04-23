# -*- coding: utf-8 -*-

import time
import pytz
from datetime import datetime


def get_current_ts_sec():
    """
    秒时间戳
    """
    return int(time.time())


def get_current_ts_ms():
    """
    毫秒时间戳
    """
    return int(time.time() * 1000)


def get_second_of_day():
    """
    获取今天的秒数
    """
    now = datetime.now()
    return now.hour*3600+now.minute*60+now.second


def get_day_of_week():
    """
    获取周几
    0:周一 1:周二 2:周三 3:周四 4:周五 5:周六 6:周日
    """
    return datetime.now().weekday()


def get_date():
    """
    获取日期
    """
    return datetime.now().date()


def get_datetime_from_str(datetime_str, tz=pytz.timezone("Asia/Shanghai"), fmt="%Y-%m-%d %H:%M:%S"):
    """
    从日期时间字符串获得datetime
    """
    try:
        dt = datetime.strptime(datetime_str, fmt)
        if tz:
            return tz.localize(dt)
        return dt
    except Exception as ex:
        return None


def get_ms_from_str(datetime_str, tz=pytz.timezone("Asia/Shanghai")):
    """
    时间字符串转毫秒时间戳
    """
    dt = get_datetime_from_str(datetime_str, tz)
    if dt is None:
        return 0
    return int(dt.timestamp()*1000+dt.microsecond/1000)


def get_ts_from_str(datetime_str, tz=pytz.timezone("Asia/Shanghai"), fmt="%Y-%m-%d %H:%M:%S"):
    """
    时间字符串转时间戳
    """
    dt = get_datetime_from_str(datetime_str, tz, fmt)
    if dt is None:
        return 0
    return int(dt.timestamp())


def get_str_from_datetime(dt, tz=pytz.timezone("Asia/Shanghai"), fmt="%Y-%m-%d %H:%M:%S"):
    """
    datetime格式化
    """
    try:
        return datetime.strftime(dt.astimezone(tz=tz), fmt)
    except Exception as ex:
        return ""


def tms_to_time_str(tms, tz=pytz.timezone("Asia/Shanghai")):
    """
    毫秒时间戳格式化
    """
    try:
        dt = datetime.fromtimestamp(tms/1000)
        if tz:
            return tz.localize(dt)
        return dt
    except Exception as ex:
        return None
