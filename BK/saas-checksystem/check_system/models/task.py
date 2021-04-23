# -*- coding: utf-8 -*-

from django.db import models

from check_system.models import CheckSystemOs
from check_system.models.tpl import Tpl


class Task(models.Model):

    task_name = models.CharField(max_length=20, default="", verbose_name="任务名称")
    task_tpl = models.ForeignKey(to=Tpl, on_delete=models.PROTECT,verbose_name="任务模板")
    task_op = models.CharField(max_length=50, default="", verbose_name="执行人")  # 自动获取执行用户名
    # 0 默认输入
    # 1 centos
    # 2 ubuntu
    # 3 suse
    # 4 windows
    task_os = models.IntegerField(default=0, verbose_name="执行系统")
    exec_biz_id = models.IntegerField(default=0, verbose_name="业务id")
    exec_hosts = models.TextField(max_length=10000, default="", verbose_name="执行的主机")
    exec_acc = models.CharField(max_length=20, default="", verbose_name="执行账户")  # 手动输入执行用户名
    exec_schedule = models.CharField(max_length=200, default="", verbose_name="执行计划")

    STATE_CHOICES = (
        (0, "未执行"),
        (1, "执行中"),
        (2, "执行完成"),
        (3, "执行错误"),
    )

    exec_state = models.IntegerField(choices=STATE_CHOICES, default=0, verbose_name="执行状态")
    exec_progress = models.IntegerField(default=0, verbose_name="执行进度")
    exec_quota_total = models.IntegerField(default=0, verbose_name="执行总指标数量")

    start_time = models.DateTimeField(verbose_name="任务开始时间")
    end_time = models.DateTimeField(null=True, verbose_name="任务结束时间")

    # 启动周期格式: 2020-12-30
    exec_start_time = models.CharField(max_length=50, null=True, default="", verbose_name='启动日期')
    # 运行周期单位为： 天
    exec_timece = models.IntegerField(null=True, default=0, verbose_name='运行周期')

    # 是否删除
    # 1 已删除 0 未删除
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    class Meta:
        verbose_name = "任务"
        verbose_name_plural = verbose_name

    def to_dict(self, bk_info_lists={}, os_info_lists={}, tpl_info_lists={}):
        task_notifys = TaskNotify.objects.filter(task_id=self.id)
        return {
            "id": self.id,
            "task_name": self.task_name,
            "task_tpl": self.task_tpl.id,
            "task_op": self.task_op,
            "task_os": self.task_os,
            "exec_hosts": eval(self.exec_hosts),
            "exec_biz_id": self.exec_biz_id,
            "exec_acc": self.exec_acc,
            "exec_schedule": self.exec_schedule,
            "exec_state": self.exec_state,
            "exec_progress": self.exec_progress,
            "exec_quota_total": self.exec_quota_total,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "",
            "exec_start_time": self.exec_start_time,
            "exec_timece": self.exec_timece,
            'is_deleted': self.is_deleted,
            'exec_biz_name': bk_info_lists[self.exec_biz_id],
            'task_os_name': os_info_lists[self.task_os],
            'task_tpl_name': tpl_info_lists[self.task_tpl.id],
            "notify_usernames": [task_notify.username for task_notify in task_notifys]
        }

    def to_dict_log(self):
        task_notifys = TaskNotify.objects.filter(task_id=self.id)
        return {
            "task_name": self.task_name,
            "task_tpl": self.task_tpl.tpl_name,
            "task_op": self.task_op,
            "task_os": self.task_os,
            "exec_hosts": eval(self.exec_hosts),
            "exec_biz_id": self.exec_biz_id,
            "exec_acc": self.exec_acc,
            "exec_schedule": self.exec_schedule,
            "exec_state": self.exec_state,
            "exec_progress": self.exec_progress,
            "exec_quota_total": self.exec_quota_total,
            "exec_start_time": self.exec_start_time,
            "exec_timece": self.exec_timece,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "",
            "notify_usernames": [task_notify.username for task_notify in task_notifys]
        }

    def to_dict_detail(self):
        task_notifys = TaskNotify.objects.filter(task_id=self.id)
        return {
            "id": self.id,
            "task_name": self.task_name,
            "task_tpl": self.task_tpl.id,
            "task_op": self.task_op,
            "task_os": self.task_os,
            "exec_hosts": eval(self.exec_hosts),
            "exec_biz_id": self.exec_biz_id,
            "exec_acc": self.exec_acc,
            "exec_schedule": self.exec_schedule,
            "exec_state": self.exec_state,
            "exec_progress": self.exec_progress,
            "exec_quota_total": self.exec_quota_total,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "",
            "exec_start_time": self.exec_start_time,
            "exec_timece": self.exec_timece,
            'is_deleted': self.is_deleted,
            "notify_usernames": [task_notify.username for task_notify in task_notifys]
        }

class TaskNotify(models.Model):
    task_id = models.IntegerField(null=False, verbose_name="任务id")
    username = models.CharField(max_length=50, null=False, verbose_name="用户名")
    is_deleted = models.PositiveIntegerField(default=0, null=False, verbose_name="是否删除")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        db_table = "check_system_task_notify"
        verbose_name = "任务通知"
        verbose_name_plural = verbose_name
