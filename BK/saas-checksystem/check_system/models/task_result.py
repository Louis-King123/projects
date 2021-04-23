# -*- coding: utf-8 -*-

import json

from django.db import models

from check_system.models.task import Task
from check_system.models.quota import Quota
from check_system.models.check_class import CheckSystemClass


class TaskResult(models.Model):
    task = models.ForeignKey(to=Task, on_delete=models.PROTECT)
    # quota = models.ForeignKey(to=Quota, on_delete=models.PROTECT)
    quota_id = models.IntegerField(null=True)
    TASK_STATE_CHOICES = (
        (0, "未执行"),
        (1, '等待中'),
        (2, "执行中"),
        (3, "执行完成"),
        (4, "查询解析完成"),
        (5, "执行失败"),
        (6, "解析失败"),
    )

    task_state = models.IntegerField(choices=TASK_STATE_CHOICES, verbose_name="步骤状态")
    task_step_state = models.IntegerField(verbose_name="作业平台的步骤状态")

    raw_log = models.TextField(max_length=10000, default="", verbose_name="原始日志")
    result = models.TextField(max_length=10000, default="", verbose_name="任务结果json")
    """
    result的示例
    {
        "ip": {
            "指标的描述": val
            "指标的描述_warning": false
        }
    }
    """

    def to_dict(self):
        result = []
        if self.result:
            result = json.loads(self.result)

        return {
            "id": self.id,
            "quota_name": self.quota_id,
            # "quota_threshold": self.quota.quota_threshold,
            "task_state": self.get_task_state_display(),
            "task_step_state": self.task_step_state,
            "result": result,
        }


class TaskHostResult(models.Model):
    host_ip = models.CharField(max_length=20, verbose_name='主机IP')
    quota_id = models.ForeignKey(Quota, on_delete=models.PROTECT)   # 脚本ID
    system_class = models.ForeignKey(CheckSystemClass, on_delete=models.PROTECT, null=True, blank=True)  # 指标类
    task_id = models.ForeignKey(Task, on_delete=models.PROTECT)     # 任务ID
    check_result = models.TextField(verbose_name='检查内容', null=True, blank=True)  # 检查内容， content
    recommend_value = models.CharField(max_length=20, verbose_name='推荐值', null=True)    # 比较值
    result_status = models.BooleanField(verbose_name='比较后结果', default=True)     # 比较后结果
    execute_log_id = models.IntegerField(verbose_name='操作日志ID', null=True, blank=True)
    os_id = models.IntegerField(verbose_name='系统ID', null=Task, blank=True)

    class Meta:
        db_table = 'check_system_task_ipresult'

    def to_dict(self):
        return {
            "id": self.id,
            "quota_id": self.quota_id,
            "quota_name": self.quota_id.quota_name,
            "system_class_id": self.system_class,
            "system_class_name": self.system_class.class_name if self.system_class else "",
            "check_result": self.check_result,
            "recommend_value": self.recommend_value,
            "result_status": self.result_status,
            "execute_log_id": self.execute_log_id
        }

    def to_json(self):
        return {
            "id": self.id,
            "quota_id": self.quota_id.id,
            "quota_name": self.quota_id.quota_name,
            "system_class_id": self.system_class.id,
            "system_class_name": self.system_class.class_name if self.system_class else "",
            "system_class_sort": self.system_class.sort,
            "check_result": self.check_result,
            "recommend_value": self.recommend_value,
            "result_status": self.result_status,
            "execute_log_id": self.execute_log_id
        }

