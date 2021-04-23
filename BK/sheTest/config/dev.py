# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from config import RUN_VER
from config.default import FRONTEND_BACKEND_SEPARATION

if RUN_VER == "open":
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 本地开发环境
RUN_MODE = "DEVELOP"

# 自定义本地环境日志级别
# from blueapps.conf.log import set_log_level # noqa
# LOG_LEVEL = "DEBUG"
# LOGGING = set_log_level(locals())

# APP本地静态资源目录
STATIC_URL = "/static/"

# APP静态资源目录url
# REMOTE_STATIC_URL = '%sremote/' % STATIC_URL

# Celery 消息队列设置 RabbitMQ
# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# Celery 消息队列设置 Redis
BROKER_URL = "redis://localhost:6379/0"

DEBUG = True

# 本地开发数据库设置
# USE FOLLOWING SQL TO CREATE THE DATABASE NAMED APP_CODE
# SQL: CREATE DATABASE `framework_py` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci; # noqa: E501
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": APP_CODE,  # noqa
#         "USER": "root",
#         "PASSWORD": "920403Love",
#         "HOST": "localhost",
#         "PORT": "3306",
#     },
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": APP_CODE,  # noqa
        "USER": "root",
        # "PASSWORD": "Ycm.616443378",
        "PASSWORD": "123456",
        "HOST": "47.117.126.142",
        # "HOST": "1.15.123.224",
        "PORT": "3306",
    },
}

# 前后端开发模式下支持跨域配置
if FRONTEND_BACKEND_SEPARATION:
    INSTALLED_APPS += ("corsheaders",)
    # 该跨域中间件需要放在前面
    MIDDLEWARE = ("corsheaders.middleware.CorsMiddleware",) + MIDDLEWARE
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True

# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings.py 加入版本管理忽略文件中
try:
    from .local_settings import *  # noqa
except ImportError:
    pass

"""
# My hosts
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1	localhost
255.255.255.255	broadcasthost
::1             localhost
# Added by Docker Desktop
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
# End of section
192.168.5.249 paas.yxkj.com job.yxkj.com cmdb.yxkj.com consul.yxkj.com
127.0.0.1 appdev.paas.bkce.com
139.186.171.166 paas.bktencent.com cmdb.bktencent.com job.bktencent.com jobapi.bktencent.com
10.0.6.24 paas.bkce.com cmdb.bkce.com job.bkce.com jobapi.bkce.com
10.0.6.25 nodeman.bkce.com
10.0.6.33 devops.bkce.com
10.0.6.37 paas.bkee.com cmdb.bkee.com job.bkee.com jobapi.bkee.com
10.0.6.39  nodeman.bkee.com
#127.0.0.1 dev.bktencent.com
# chengdu bkce
#106.75.18.253 paas.bktencent.com cmdb.bktencent.com job.bktencent.com jobapi.bktencent.com
"""