# -*- coding: utf-8 -*-

from django.views import View
from django.core.paginator import Paginator

from check_system.common.request import Request
from check_system.common.utils import get_post_params
from check_system.models import CheckSystemOs


class InspectionObject(View):

    def get(self, request):
        # 分页参数
        current = request.GET.get("current", 0)
        limit = request.GET.get("limit", 0)
        os_name = request.GET.get("os_name", "")

        # 封装查询参数
        kwargs = {"is_deleted": 0}
        if os_name:
            kwargs['os_name__icontains'] = os_name

        system_os = CheckSystemOs.objects.filter(**kwargs)

        if current and limit:
            paginator = Paginator(system_os.order_by('id'), int(limit))
            count = paginator.count
            data = [os.to_dict() for os in paginator.page(int(current))]
        else:
            count = system_os.count()
            data = [os.to_dict() for os in system_os.order_by('id')]
        return Request.succFcun('', data={"count": count, "data": data})

    def post(self, request):
        req = get_post_params(request)
        os_name = req.get("os_name", "")
        os_id = req.get("os_id", 0)
        is_deleted = int(req.get("is_deleted", 0))

        if not os_name and is_deleted == "":
            return Request.errorFcun("参数异常", data=[])

        data = {
            "os_name": os_name,
            "is_deleted": is_deleted
        }

        # 如果id 存在更新
        if os_id:
            os_obj = CheckSystemOs.objects.get(pk=os_id)
            os_obj.__dict__.update(**data)
            os_obj.save()

            if os_obj and is_deleted == 1:
                result_message = "删除成功"
            else:
                result_message = "修改成功"
        else:
            os_obj, created = CheckSystemOs.objects.get_or_create(defaults=data, os_name=os_name)
            if created:
                result_message = "创建成功"
            else:
                result_message = "数据已存在"

        if os_obj:
            return Request.succFcun(result_message, data=os_obj.to_dict())
        else:
            return Request.errorFcun("创建/更新失败", data={})
