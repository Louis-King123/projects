# -*- coding: utf-8 -*-
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from app.utils.util_req_resp import json_resp, parse_json
from app.models import OrgCode
from app.utils.util_page_number import get_actual_page


@require_http_methods(["POST"])
def fetch_org_code_list(request):
    """
    获取各分局公安机关机构代码列表
    :param request:
    :return:
    """
    req_params = parse_json(request)
    limit = req_params.get('limit', 50)
    current_page = req_params.get('page', 1)
    try:
        org_code = OrgCode.objects.all().order_by("-id")
        current_page = get_actual_page(len(org_code), limit, current_page)
        paginator = Paginator(org_code, limit)
        org_code = paginator.page(current_page)
        data_list = []
        data = {
            'count': 0,
            'list': [],
            'current_page': current_page
        }
        if org_code:
            for item in org_code:
                data_list.append({
                    "id": item.id,
                    "name": item.name,
                    "code": item.code
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