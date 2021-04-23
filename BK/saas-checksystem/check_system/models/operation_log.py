# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CheckSystemOperationLog(models.Model):
    username = models.CharField(default='admin', max_length=100, verbose_name='用户名')
    remote_address = models.CharField(default='', max_length=100, verbose_name='客户端地址')
    request_method = models.CharField(default='', max_length=40, verbose_name='请求方式')
    request_path = models.CharField(default='', max_length=100, verbose_name='请求路由')
    operation_module = models.CharField(default='', max_length=100, verbose_name='操作模块')
    operation_description = models.TextField(blank=True, null=True, verbose_name='操作描述')

    request_data = models.TextField(blank=True, null=True, verbose_name='请求参数')
    change_detail = models.TextField(blank=True, null=True, verbose_name='更改细节')
    request_time = models.DateTimeField(verbose_name='请求时间')
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True,null=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True,null=True, verbose_name='修改时间')

    class Meta:
        db_table = 'check_system_operation_log'

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "request_method": self.request_method,
            "operation_module": self.operation_module,
            "operation_description": self.operation_description,
            "request_data": self.request_data,
            "change_detail": eval(self.change_detail),
            "request_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
