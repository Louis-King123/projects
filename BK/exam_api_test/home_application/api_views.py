# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from django.http import JsonResponse
from django.conf import settings
from blueking.component.client import ComponentClient


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

# ###########  蓝鲸统一登陆 ##############
# 获取登陆用户信息
class BkLogin(object):

    @classmethod
    def get_user(cls, request):
        bk_app_code = settings.APP_CODE
        bk_app_secret = settings.SECRET_KEY
        bk_token = request.COOKIES['bk_token']  # bk_token

        # 获取client方法1
        # client = get_client_by_request(request)

        # 获取client方法2
        client = ComponentClient(
            bk_app_code=bk_app_code,
            bk_app_secret=bk_app_secret,
            common_args={'bk_token': bk_token}
        )

        info = client.bk_login.get_user()
        print(info['data']['bk_username'])  # 用户名
        print(info['data']['email'])  # 邮箱
        return JsonResponse(info)


# ###########  蓝鲸开发者中心 ##############
# 获取应用信息
class GetAppInfo(object):

    @classmethod
    def get_app_info(cls, request):
        client = get_client_by_request(request)
        info = client.bk_paas.get_app_info()
        all_apps = info['data']
        for app in all_apps:
            print(app['bk_app_code'])
            print(app['bk_app_name'])
            print('*'*30)
        return JsonResponse(info)


# ###########  蓝鲸消息管理 ##############
class PaasCmsi(object):

    @classmethod
    def get_msg_type(cls, request):
        """
        查询消息发送类型
        """
        client = get_client_by_request(request)
        info = client.cmsi.get_msg_type()
        alls = info['data']
        for app in alls:
            print(app['is_active'])
            print(app['label'])
            print(app['type'])
            print('*'*30)
        return JsonResponse(info)

    @classmethod
    def send_mail(cls, request):
        """
        发送邮件
        """
        receiver = request.GET.get('receiver')
        title = request.GET.get('title')
        content = request.GET.get('content')
        client = get_client_by_request(request)

        kwargs = {
            "receiver": receiver,
            # "receiver": "shexiaolong@tenyuns.com",
            "title": title,
            # "title": "shexiaolong",
            "content": "<html>"+content+"</html>",
            # "content": "<html>shexiaolong email send test</html>",
        }

        info = client.cmsi.send_mail(kwargs)
        return JsonResponse(info)

    @classmethod
    def send_sms(cls, request):  # TODO
        """
        发送短信
        """
        receiver = request.GET.get('receiver')
        content = request.GET.get('content')
        client = get_client_by_request(request)

        kwargs = {
            "receiver": receiver,
            # "receiver": "18701730286",
            "content": content,
            # "content": "shexiaolong sms send test",
        }

        info = client.cmsi.send_sms(kwargs)
        return JsonResponse(info)

    @classmethod
    def send_weixin(cls, request):  # TODO
        """
        发送微信
        """
        heading = request.GET.get('heading')
        message = request.GET.get('message')
        remark = request.GET.get('remark')
        client = get_client_by_request(request)

        kwargs = {
            "receiver": "18701730286",
            "data": {
                "heading": heading,
                # "heading": "blueking alarm",
                "message": message,
                # "message": "This is a test.",
                "remark": remark
                # "remark": "This is a test!"
            }
        }

        info = client.cmsi.send_weixin(kwargs)
        return JsonResponse(info)


# ###########  用户管理 ##############
class UserManager(object):

    @classmethod
    def list_users(cls, request):
        """查询用户"""
        client = get_client_by_request(request)
        kwargs = {
            "no_page": True
            # "fields": "username,id",
        }

        info = client.usermanage.list_users(kwargs)
        """
        所有字段
        "status": "NORMAL", 
        "domain": "default.local", 
        "telephone": "", 
        "create_time": "2021-01-05T10:16:38.004808Z", 
        "country_code": "86", 
        "logo": null, 
        "iso_code": "CN", 
        "id": 1, 
        "display_name": "", 
        "leader": null,
        "username": "admin", 
        "update_time": "2021-04-16T03:00:08.503830Z",
        "wx_userid": "", "staff_status": "IN",
        "password_valid_days": -1，
        "qq": "", 
        "language": "zh-cn",
        "enabled": true,
        "time_zone": "Asia/Shanghai",
        "departments": 1, 
        "email": "", 
        "extras": "{}", 
        "position": 0,
        "category_id": 1
        """
        return JsonResponse(info)

    @classmethod
    def list_departments(cls, request):
        """查询部门"""
        client = get_client_by_request(request)
        kwargs = {
            "no_page": True
            # "fields": "name,id",
        }

        info = client.usermanage.list_departments(kwargs)
        """
        所有字段
        "rght": 4,
        "code": null, 
        "name": "\u603b\u516c\u53f8",
        "parent": null, 
        "level": 0,
        "has_children": false,
        "enabled": true, 
        "id": 1, "lft": 1,
        "extras": {},
        "full_name": "\u603b\u516c\u53f8", 
        "tree_id": 1, 
        "category_id": 1,
        "order": 1
        """
        return JsonResponse(info)


