# -*- coding: utf-8 -*-
from django.conf.urls import url

from check_system.apis.inspection_report import InspectionReport, HistoryReport, InspectionReportDetail

urlpatterns = [
    url(r'^fetch_inspection_report', InspectionReport.as_view(), name='fetch_inspection_report'),  # 根据历史报告的ID获取巡检报告的详情
    url(r'^fetch_history_report', HistoryReport.as_view(), name='fetch_history_report'),  # 获取历史报告
    url(r'^fetch_inspection_detail', InspectionReportDetail.as_view(), name='fetch_inspection_detail'),  # 获取历史报告详情
]
