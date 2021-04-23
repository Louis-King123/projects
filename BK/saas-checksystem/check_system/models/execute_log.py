# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class ExecuteLog(models.Model):
    work_code = models.CharField(max_length=50, verbose_name='条形码')
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    end_time = models.DateTimeField(null=True, verbose_name='结束时间')
    STATE_CHOICES = (
        (0, "未执行"),
        (1, "执行中"),
        (2, "执行完成"),
        (3, "执行错误"),
    )

    exec_state = models.IntegerField(choices=STATE_CHOICES, default=0, verbose_name="执行状态")
    task_id = models.IntegerField(default=0, null=True, verbose_name='任务ID')
    operator = models.CharField(max_length=50, default='geshuying', null=True, verbose_name='执行人')

    class Meta:
        db_table = 'check_system_execute_log'

    def to_dict(self):
        return {
            "id": self.id,
            "work_code": self.work_code,
            "is_deleted": self.is_deleted,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_time": self.updated_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "exec_state": self.exec_state,
            "task_id": self.task_id,
            "operator": self.operator
        }
