import time

from django.core.paginator import Paginator
from check_system.common.request import Request
from check_system.common.utils import get_now_time
from check_system.models.operation_log import CheckSystemOperationLog


def operation_log(request):
    current = request.GET.get("current", 1)
    limit = request.GET.get("limit", 10)
    start_time = request.GET.get("start_time", "1970-01-01")
    end_time = request.GET.get("end_time", time.strftime("%Y-%m-%d", time.localtime()))

    usernames = request.GET.get("operator[]", '')

    start_time = start_time + " 00:00:00"
    end_time = end_time + " 23:59:59"
    kwargs = {
        'operation_module': request.GET.get("operation_module", ""),
        'request_method': request.GET.get("request_method", ""),
        'request_time__range': [start_time, end_time]
    }
    if usernames:
        kwargs['username__in'] = usernames.split(",")

    # 删除空值项
    for key_str in list(kwargs.keys()):
        if not kwargs[key_str]:
            kwargs.pop(key_str)

    logs = CheckSystemOperationLog.objects.filter(**kwargs).order_by("-created_time")

    paginator = Paginator(logs, int(limit))
    data = [log.to_dict() for log in paginator.page(int(current))]
    return Request.succFcun('', data={"count": paginator.count, "data": data})
