from check_system.models import Quota
from check_system.models.models import CheckSystemTplQuta


class TplLogic:
    def getQuotas(self, tpl_id):
        # 模板和配置中间表

        # 获取模板表实例数据
        quotaData = CheckSystemTplQuta.objects.filter(tpl_id=tpl_id)

        # 模板和配置中间表
        qupta_ids = []
        qupta_map_value = {}
        val = {}

        for val in quotaData:

            qupta_ids.append(val.quota_id)
            # 创建比对值dict
            qupta_map_value[val.quota_id] = val.quota_threshold

        del val

        quotas = Quota.objects.filter(id__in=qupta_ids)

        data = []
        for val in quotas:
            temp = val.to_dict()
            if qupta_map_value[val.id] != '':
                temp["quota_threshold"] = qupta_map_value[val.id]
            data.append(temp)
        return data
