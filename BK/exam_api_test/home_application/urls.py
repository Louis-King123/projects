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

from . import views, api_views, peizhi_pingtai, zuoye_pingtai

urlpatterns = (
    url(r"^$", api_views.BkLogin.get_user),
    # url(r"^$", views.home),
    # url(r"^dev-guide/$", views.dev_guide),
    # url(r"^contact/$", views.contact),
    # -------------------------------
    url(r"^login-user/$", api_views.BkLogin.get_user),  # 获取登陆用户信息
    url(r"^paas-app-info/$", api_views.GetAppInfo.get_app_info),  # 获取应用信息
    url(r"^get-msg-type/$", api_views.PaasCmsi.get_msg_type),  # 查询消息发送类型
    url(r"^send-mail/$", api_views.PaasCmsi.send_mail),  # 发送邮件
    url(r"^send-sms/$", api_views.PaasCmsi.send_sms),  # 发送短信
    url(r"^send-weixin/$", api_views.PaasCmsi.send_weixin),  # 发送微信
    # -------------------------------
    url(r"^user-lists/$", api_views.UserManager.list_users),  # 查询用户
    url(r"^list-departments/$", api_views.UserManager.list_departments),  # 查询部门
    # ------------------------------配置平台
    url(r"^create-business/$", peizhi_pingtai.ConfigPlatform.create_business),  # 新建业务

    url(r"^search-business/$", peizhi_pingtai.ConfigPlatform.search_business),  # 查询业务
    url(r"^search-biz-inst-topo/$", peizhi_pingtai.ConfigPlatform.search_biz_inst_topo),  # 查询业务实例拓扑 根据业务ID
    url(r"^search-biz-set/$", peizhi_pingtai.ConfigPlatform.search_biz_set),  # 根据业务ID获取集群
    url(r"^search-biz-set-module/$", peizhi_pingtai.ConfigPlatform.search_biz_set_module),  # 根据业务ID,集群ID，获取模块信息

    url(r"^list-biz-hosts/$", peizhi_pingtai.ConfigPlatform.list_biz_hosts),  # 查询业务下的主机
    url(r"^get-host-base-info/$", peizhi_pingtai.ConfigPlatform.get_host_base_info),  # 根据主机ID获取主机详情

    url(r"^list-service-template/$", peizhi_pingtai.ConfigPlatform.list_service_template),  # 服务模板列表查询 根据业务 id 查询服务模板列表
    url(r"^get-service-template/$", peizhi_pingtai.ConfigPlatform.get_service_template),  # 根据服务模板 ID 获取服务模板
    url(r"^list-set-template/$", peizhi_pingtai.ConfigPlatform.list_set_template),  # 根据业务 id 查询服务实例列表,也可以加上模块 id 等信息查询
    url(r"^create-service-template/$", peizhi_pingtai.ConfigPlatform.create_service_template),  # 根据传入的服务模板名称的服务分类 ID 创建指定名称和服务分类的服务模板
    url(r"^update-service-template/$", peizhi_pingtai.ConfigPlatform.update_service_template),  # 更新服务模板 更新服务模板名称信息
    url(r"^delete-service-template/$", peizhi_pingtai.ConfigPlatform.delete_service_template),  # 删除服务模板 根据服务模板 ID 删除服务模板

    url(r"^find-host-biz-relations/$", peizhi_pingtai.ConfigPlatform.find_host_biz_relations),  # 查询主机业务关系信息 根据主机 ID 查询业务相关信息
    url(r"^list-resource-pool-hosts/$", peizhi_pingtai.ConfigPlatform.list_resource_pool_hosts),  # 查询资源池中的主机
    url(r"^list-service-instance/$", peizhi_pingtai.ConfigPlatform.list_service_instance),  # 根据业务 id 查询服务实例列表,也可以加上模块 id 等信息查询

    # url(r"^search-topo-tree/$", peizhi_pingtai.ConfigPlatform.search_topo_tree),
    url(r"^add-host-to-resource/$", peizhi_pingtai.ConfigPlatform.add_host_to_resource),  # 新增主机到资源池
    url(r"^delete-host/$", peizhi_pingtai.ConfigPlatform.delete_host),  # 删除主机

    url(r"^add-host-lock/$", peizhi_pingtai.ConfigPlatform.add_host_lock),  # 根据主机的 id 列表对主机加锁，新加主机锁，如果主机已经加过锁，同样提示加锁成功
    url(r"^delete-host-lock/$", peizhi_pingtai.ConfigPlatform.delete_host_lock),  # 根据主机 ID 删除主机锁，多个以逗号分隔

    url(r"^clone-host-property/$", peizhi_pingtai.ConfigPlatform.clone_host_property),  # 克隆主机属性

    url(r"^list-service-category/$", peizhi_pingtai.ConfigPlatform.list_service_category),  # 查询服务分类列表，根据业务 ID 查询
    url(r"^create-service-category/$", peizhi_pingtai.ConfigPlatform.create_service_category),  # 创建服务分类
    url(r"^delete-service-category/$", peizhi_pingtai.ConfigPlatform.delete_service_category),  # 删除服务分类
    url(r"^update-service-category/$", peizhi_pingtai.ConfigPlatform.update_service_category),  # 更新服务模板信息（目前仅名称字段可更新）

    # ------------------------------作业平台
    url(r"^get-account-list/$", zuoye_pingtai.ZuoYePlatform.get_account_list),  # 查询业务下的执行账号 查询业务下用户有权限的执行账号列表
    url(r"^get-cron-list/$", zuoye_pingtai.ZuoYePlatform.get_cron_list),  # 查询业务下定时作业信息
    url(r"^get-cron-detail/$", zuoye_pingtai.ZuoYePlatform.get_cron_detail),  # 查询定时作业详情
    url(r"^save-cron/$", zuoye_pingtai.ZuoYePlatform.save_cron),  # 新建定时任务
    url(r"^get-job-plan-list/$", zuoye_pingtai.ZuoYePlatform.get_job_plan_list),  # 查询执行方案列表
    url(r"^get-job-plan-detail/$", zuoye_pingtai.ZuoYePlatform.get_job_plan_detail),  # 根据作业执行方案 ID 查询作业执行方案详情
    url(r"^update-cron-status/$", zuoye_pingtai.ZuoYePlatform.update_cron_status),  # 更新定时任务状态
    url(r"^save-cron-update/$", zuoye_pingtai.ZuoYePlatform.save_cron_update),  # 更新定时任务
    url(r"^execute-job-plan/$", zuoye_pingtai.ZuoYePlatform.execute_job_plan),  # 执行作业执行方案
    url(r"^get-job-instance-status/$", zuoye_pingtai.ZuoYePlatform.get_job_instance_status),  # 根据作业实例 ID 查询作业执行状态
    url(r"^get-job-instance-ip-log/$", zuoye_pingtai.ZuoYePlatform.get_job_instance_ip_log),  # 根据作业实例 ID 查询作业执行日志 根据ip查询作业执行日志
    url(r"^execute-job-and-get-log/$", zuoye_pingtai.DoJobPlan.execute_job_and_get_log),  # 练习
)
