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

from django.conf.urls import url

from check_system.apis.config import NotifyConfig
from check_system.apis.inspection_os import InspectionObject
from check_system.apis.operation_log import operation_log
from check_system.apis.tpl import *
from check_system.apis.quota import *
from check_system.apis.bk import *
from check_system.apis.task import *
from check_system.apis.report import *
from check_system.apis.home import *





urlpatterns = (
    # 蓝鲸
    url(r"^fetch_host_list", fetch_host_list),
    url(r"^search_host_by_biz", search_host_by_biz),

    # 模板
    url(r"^get_os_list", get_os_list),
    url(r"^fetch_tpl_list", fetch_tpl_list),
    url(r"^tpl", Tpl_View.as_view()),
    url(r"^execute_tpl", execute_tpl),

    # 任务
    url(r"^task_add", task_add),
    url(r"^execute_task", execute_task),

    # 指标
    url(r"^fetch_quota_by_tpl", fetch_quota_by_tpl),

    url(r"^quota", Quota_View.as_view()),
    url(r"^featch_os_quota", fetch_os_quota),
    url(r"^add_quota", add_quota),

    # 任务报告
    url(r"^fetch_report", fetch_report),

    # 新增任务
    url(r"^business_hosts", business_hosts),
    url(r"^hosts_topo", TopoHost),
    url(r"^business_list", business_list),

    # 任务列表
    url(r"^task_detail", task_detail),
    url(r"^fetch_task_list", fetch_task_list),
    url(r"^task_delete", task_delete),
    url(r"^off_button", off_button),


    url(r"^operation_log", operation_log),

    url(r"^fetch_check_activity", fetch_check_activity),

    url(r"^fetch_check_statistics", fetch_check_statistics),

    url(r"^fetch_user_list", fetch_user_list),

    url(r"^notify_config", NotifyConfig.as_view()),
    url(r"^inspection_os", InspectionObject.as_view()),
)
