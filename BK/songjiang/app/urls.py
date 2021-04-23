# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import views, base_soft_data, cloud_data_all, cloud_serve_type, pc_room_data,\
    police_wechat_data, report_log, server_data, server_data_all, soft_data, org_code
urlpatterns = (
    url(r"^index$", views.index),
    url(r"^test$", views.test),
    url(r"^basesoft/fetch_base_soft_list$", base_soft_data.fetch_base_soft_list),
    url(r"^basesoft/delete_base_soft", base_soft_data.delete_base_soft),
    url(r"^basesoft/update_base_soft$", base_soft_data.update_base_soft),
    url(r"^basesoft/add_base_soft", base_soft_data.add_base_soft),
    url(r"^clouddata/fetch_cloud_data_list$", cloud_data_all.fetch_cloud_data_list),
    url(r"^clouddata/update_cloud_data$", cloud_data_all.update_cloud_data),
    url(r"^clouddata/delete_cloud_data$", cloud_data_all.delete_cloud_data),
    url(r"^clouddata/add_cloud_data$", cloud_data_all.add_cloud_data),
    url(r"^cloudserve/fetch_cloud_serve_type_list$", cloud_serve_type.fetch_cloud_serve_type_list),
    url(r"^cloudserve/update_cloud_serve_type$", cloud_serve_type.update_cloud_serve_type),
    url(r"^cloudserve/delete_cloud_serve_type$", cloud_serve_type.delete_cloud_serve_type),
    url(r"^cloud_serve_type/add_cloud_serve_type", cloud_serve_type.add_cloud_serve_type),
    url(r"^pcroom/fetch_pc_room_data_list$", pc_room_data.fetch_pc_room_data_list),
    url(r"^pcroom/update_pc_room_data$", pc_room_data.update_pc_room_data),
    url(r"^pcroom/delete_pc_room_data", pc_room_data.delete_pc_room_data),
    url(r"^policewechat/fetch_police_wechat_data_list$", police_wechat_data.fetch_police_wechat_data_list),
    url(r"^policewechat/update_police_wechat_data$", police_wechat_data.update_police_wechat_data),
    url(r"^reportlog/fetch_report_log_list$", report_log.fetch_report_log_list),
    url(r"^serverdata/fetch_server_data_list$", server_data.fetch_server_data_list),
    url(r"^serverdata/update_server_data$", server_data.update_server_data),
    url(r"^serverdataall/fetch_server_data_all_list$", server_data_all.fetch_server_data_all_list),
    url(r"^serverdataall/update_server_data_all$", server_data_all.update_server_data_all),
    url(r"^serverdataall/get_avg_indicators", server_data_all.get_avg_indicators),
    url(r"^softdata/fetch_soft_data_list$", soft_data.fetch_soft_data_list),
    url(r"^soft_data/update_soft_data$", soft_data.update_soft_data),
    url(r"^orgcode/fetch_org_code_list$", org_code.fetch_org_code_list)
)

