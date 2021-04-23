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

from . import views
from . import modify_time

urlpatterns = (
    # url(r'^$', views.home),
    url(r'^$', views.home_index),
    url(r'^history/$', views.history),
    url(r'^history_info/$', views.history_info),
    url(r'^api/test/$', views.api_test),
    url(r'^business/$', views.all_business),
    url(r'^list_topo_hosts/$', views.list_topo_hosts),
    url(r'^fast_exce_script/$', views.fast_exce_script),
    url(r'^search_topo/$', views.search_topo),
    # url(r'^list_biz_hosts/$', views.list_biz_hosts),
    url(r'^execute_backup/$', views.execute_backup),

    url(r'^test_add_task/$', modify_time.test_add_task),
)
