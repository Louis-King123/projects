# -*- coding: utf-8 -*-
import base64
import json
import time
from datetime import datetime

import pytz
from django.utils import timezone

from blueapps.utils.logger import logger
from blueking.component.shortcuts import get_client_by_request, get_client_by_user
from check_system.common.req import req_body_to_json


def get_all_biz(request):
    """
    获取所有业务业务
    """
    client = get_client_by_request(request)
    date = {
        "page": {
            "start": 0,
            "limit": 1000
        }
    }
    result = client.cc.search_business(date)

    return result


def get_post_params(request):
    try:
        req = req_body_to_json(request)
    except:
        req = request.POST
    return req

# USE_TZ = False时，此函数不使用
def get_now_time(time_str):
    """
    @time_str:无时区的时间字符串
    return ：2021-01-26 09:05:20 修改时区后的时间字符串
    """
    # 将不具有时区信息的时间转换成具有当前时区时间
    time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    tzname = timezone.get_current_timezone_name()
    time_zone_obj = pytz.timezone(tzname).localize(time_obj)

    return time_zone_obj.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")


def save_json(filename, data):
    with open(f"{filename}.json", "w", encoding="utf-8")as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def get_user_detail(username):
    """
    param:username  用户名
    return：{"email","XXXX@Gmail.com","telephone":""}
    """
    client = get_client_by_user("admin")
    kwargs = {
        "id": f"{username}",
    }
    res = client.usermanage.retrieve_user(kwargs)

    result = {"result": res['result'], "message": res['message']}
    if res.get("result", False):
        result.update({
            'username': res['data']['username'],
            'email': res['data']['email'],
            'telephone': res['data']['telephone'],
            'qq': res['data']['qq'],
            'wx_openid': res['data']['wx_openid'],
            'wx_userid': res['data']['wx_userid']
        })
    else:
        logger.warning(f"获取用户信息失败  接口名称(retrieve_user) 请求参数({kwargs})")

    return result


class Send:
    """
    发送类
    """

    def __init__(self):
        self.client = get_client_by_user("admin")
        self.send_type = {"mail": self.send_mail, "sms": self.send_sms, "weixin": self.send_weixin}

    def send_mail(self, receiver="", receiver__username="", sender="", title="", content=""):
        """
        :receiver 接收人 多个以逗号分隔,
        :receiver__username 接收人，以receiver优先 ,
        :sender 发送人,
        :title 标题,
        :content 内容,
        """
        kwargs = {
            "sender": sender,
            "title": title,
            "content": content,
            "body_format": "Text"
        }
        if receiver:
            kwargs["receiver"] = receiver
        else:
            kwargs["receiver__username"] = receiver__username

        res = self.client.cmsi.send_mail(kwargs)
        if not res.get("result", False):
            logger.warning(f"发送邮件失败  接口名称(send_mail) 请求参数({kwargs})")
        return {
            "message": res['message'],
            "result": res['result']
        }

    def send_sms(self, receiver="", receiver__username="", content=""):
        """
        :receiver 接收人 多个以逗号分隔,
        :receiver__username 接收人，以receiver优先 ,
        :title 标题,
        :content 内容,
        """
        kwargs = {
            "content": content,
        }

        if receiver:
            kwargs["receiver"] = receiver
        else:
            kwargs["receiver__username"] = receiver__username

        res = self.client.cmsi.send_sms(kwargs)
        if not res.get("result", False):
            logger.warning(f"发送信息失败  接口名称(send_sms) 请求参数({kwargs})")
        return {
            "message": res['message'],
            "result": res['result']
        }

    def send_weixin(self, receiver="", receiver__username="", heading="", message="", remark=""):
        """
        @receiver：接收人 多个以逗号分隔,
        @receiver__username：接收人，以receiver优先,
        @heading：信息头部,
        @message：信息头部,
        @remark：内容,
        """
        kwargs = {
            "data": {
                "heading": heading,  # 通知头部文字
                "message": message,  # 通知文字
                "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "remark": remark  # 通知尾部文字
            }
        }
        if receiver:
            kwargs["receiver"] = receiver
        else:
            kwargs["receiver__username"] = receiver__username

        res = self.client.cmsi.send_weixin(kwargs)
        if not res.get("result", False):
            logger.warning(f"发送微信失败  接口名称(send_weixin) 请求参数({kwargs})")
        return {
            "message": res['message'],
            "result": res['result']
        }

    def __getattr__(self, item):
        if item in self.send_type:
            return self.send_type[item]
        else:
            return None


send = Send()
