# -*- coding: utf-8 -*-
import json
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import ReportLog
from app.utils.util_page_number import get_actual_page


@require_http_methods(["POST"])
def fetch_report_log_list(request):
    """
    获取上报日志数据
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 20)
    current_page = req_params.get('page', 1)
    create_time_range = req_params.get("create_time_range")
    update_time_range = req_params.get("update_time_range")
    try:
        report_log = ReportLog.objects.all().order_by("-id")
        if update_time_range is not None and len(update_time_range):
            satm = update_time_range[0]
            edtm = update_time_range[1]
            report_log = report_log.filter(updatedTime__range=(satm, edtm))
        if create_time_range is not None and len(create_time_range) == 2:
            satm = create_time_range[0]
            edtm = create_time_range[1]
            report_log = report_log.filter(createdTime__range=(satm, edtm))
        current_page = get_actual_page(len(report_log), limit, current_page)
        paginator = Paginator(report_log, limit)
        report_log = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if report_log:
            for item in report_log:
                print(type(item.requestData))
                data_list.append({
                    "id": item.id,
                    "reportType": item.reportType,
                    "requestData": item.requestData,
                    "resultData": json.loads(item.resultData),
                    "createdTime": item.createdTime.strftime("%Y-%m-%d %H:%M:%S") if item.createdTime else None,
                    "updatedTime": item.updatedTime.strftime("%Y-%m-%d %H:%M:%S"),
                })
            data = {
                'count': paginator.count,
                'list': data_list,
                'current_page': current_page
            }
        return json_resp("success", data)
    except Exception as e:
        print(e)
        return json_resp("error", None, 500)
