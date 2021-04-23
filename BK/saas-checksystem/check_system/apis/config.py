from django.db import transaction
from django.views import View

from blueapps.utils.logger import logger
from check_system.common.req import req_body_to_json
from check_system.common.request import Request
from check_system.models.models import SystemConfig


class NotifyConfig(View):

    def get(self, request):
        notify_conf = SystemConfig.objects.filter(config_type="消息通知").values("config_value", "description")[0]
        config_values = notify_conf["config_value"].split(",")
        description = notify_conf["description"].split(",")
        notify_keys = ["type", "name"]
        descriptions = [dict(zip(notify_keys, desc.split(":"))) for desc in description]

        return Request.succFcun('', data={"config_values": config_values, "descriptions": descriptions})

    def put(self, request):
        req = req_body_to_json(request)
        notify_configs = req.get("notify_configs")
        config_value = ",".join(notify_configs)
        try:
            # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
            with transaction.atomic():
                SystemConfig.objects.filter(config_type="消息通知").update(**{"config_value": config_value})
        except:
            logger.error(f"修改通知配置  接口名称({request.path}) 请求参数({req_body_to_json(request)})")
        notify_conf = SystemConfig.objects.filter(config_type="消息通知").first()
        if notify_conf.config_value == config_value:
            return Request.succFcun('更改通知配置成功', data=[])
        else:
            return Request.errorFcun('更改通知配置失败', data=[])
