import json
import time

from django.db import transaction

from check_system.common.quota_class import tpl_quotas
from check_system.models.tpl import Tpl
from check_system.models.models import CheckSystemTplQuta, CheckSystemOs
from check_system.models.operation_log import CheckSystemOperationLog

# 参考值
Operation_module = {
    "tpl": {"model": Tpl, "message": "模板管理", "id_key": "tpl_id", "middle_table": CheckSystemTplQuta,
            "middle_value": "quotas"},

}


def process_view(module_name=''):
    def func_outer(func):
        def wrapper(request, *args, **kwargs):
            if request.META.get('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']

            # 初始化请求参数
            before_request = dict()
            request_data = dict()
            after_request = dict()

            if request.method in ["GET", "DELETE"]:
                for query_k, query_v in request.GET.items():
                    request_data[query_k] = query_v
            else:
                request_data.update(json.loads(request.body.decode()))

            # POST 不需要查询id
            if request.method == "POST":

                # 请求后修改的数据
                after_request.update(request_data)
            else:
                # 根据指定的key 拿到id
                id_key = Operation_module[module_name]['id_key']
                id = request_data.get(id_key)
                # 查询对应数据库对应id 的数据对象
                data_obj = Operation_module[module_name]['model'].objects.get(pk=id)
                # 请求前原数据
                before_request = data_obj.to_dict_log()

                # 如果存在中间表
                if "middle_table" in Operation_module[module_name]:
                    middle_value = Operation_module[module_name]['middle_value']
                    before_request[middle_value] = [data.to_dict_log() for data in
                                                    Operation_module[module_name]['middle_table'].objects.filter(
                                                        **{id_key: id}).all()]

                # 请求后修改的数据
                after_request.update(request_data)
                after_request.pop(id_key)

            log_data = {
                'username': request.user.username,
                'remote_address': ip,
                'request_method': request.method,
                'request_path': request.path,
                'request_data': json.dumps(request_data),
                'before_request': json.dumps(before_request),
                'after_request': json.dumps(after_request),
                'request_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            # print(log_data)
            # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
            with transaction.atomic():
                CheckSystemOperationLog.objects.create(**log_data)
            return func(request, *args, **kwargs)

        return wrapper

    return func_outer


class Log:
    # 请求描述
    method_desc={"POST":"新增","PUT":"修改","DELETE":"删除","EXECUTE":"执行"}
    # 操作字段
    operation_field = {"模板管理": "tpl_name", "自定义巡检": "quota_name", "任务管理": "task_name"}

    @classmethod
    def get_model_field(cls, model_name):
        """获取model 指定字段的 verbose_name属性值"""
        field_dic = {}
        for field in model_name._meta.fields:
            field_dic[field.name] = field.verbose_name
        field_dic.pop("id")
        field_dic.pop("is_deleted")
        field_dic.pop("created_time")
        field_dic.pop("updated_time")
        return field_dic

    @classmethod
    def __different_key(cls, old_dict, new_dict):
        """
        抛出两个字典中value不一样的key
        @old_dict: 旧字典
        @new_dict: 新字典
        """
        different_keys = list()
        for key in new_dict:
            if key in old_dict:
                if str(new_dict[key]) != str(old_dict[key]):
                    different_keys.append(key)
            else:
                print('无key %s' % key)

        return different_keys

    @classmethod
    def operation_log(cls, request,table_name,old_model_object=None,field_names = None,update_fields=None, operation_module_name='',method = None):
        """
        @request 上下文对象
        @old_model_object 旧模型对象
        @field_names 字段名称
        @update_fields 更新的字段
        @operation_module_name 操作类型名称
        @method 自定义方式
        """
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        request_data = dict()
        old_data = dict()

        if request.method in ["GET", "DELETE"]:
            for query_k, query_v in request.GET.items():
                request_data[query_k] = query_v
        else:
            request_data.update(json.loads(request.body.decode()))

        # 请求方式
        request_method = request.method
        # 如果有自定义方式
        if method:
            request_method = method

        # 如果存在old_orm 对象
        if old_model_object:
            old_data = old_model_object.to_dict_log()

        if operation_module_name == "模板管理" and request_method in ["PUT","DELETE"]:
            old_data['quotas'] = tpl_quotas([data.to_dict_log() for data in CheckSystemTplQuta.objects.filter(tpl_id= request_data.get("tpl_id")).all()])
            old_data['tpl_os'] = CheckSystemOs.objects.get(pk=old_data['tpl_os']).os_name

        if operation_module_name == "任务管理" and request_method in ["PUT","DELETE"]:
            pass
            # print(old_data['task_os'])
            # old_data['task_os'] = CheckSystemOs.objects.get(pk=old_data['task_os']).os_name

        change_detail= list()
        if field_names:
            for field_name,verbose_name in field_names.items():
                change_detail.append({
                    "verbose_name": verbose_name,
                    "before": old_data.get(field_name,"--"),
                    "after": update_fields.get(field_name,"--"),
                })

        if request_method == 'POST':
            change_name = update_fields[cls.operation_field[operation_module_name]]
        else:
            change_name = old_data[cls.operation_field[operation_module_name]]

        # 预置描述 方便后期扩展
        description = cls.method_desc[request_method] + table_name + f" 【{change_name}】"

        log_data = {
            'username': request.user.username,
            'remote_address': ip,
            'request_method': request_method,
            'request_path': request.path,
            'operation_module': operation_module_name,
            'operation_description': description,
            'request_data': json.dumps(request_data,indent=4,ensure_ascii=False),
            'change_detail': json.dumps(change_detail,indent=4,ensure_ascii=False),
            'request_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        # 下面的代码在一个事务中执行，一但出现异常，整个with函数内部的数据库操作都会回滚
        with transaction.atomic():
            CheckSystemOperationLog.objects.create(**log_data)