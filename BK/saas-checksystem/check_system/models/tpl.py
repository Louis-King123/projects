# -*- coding: utf-8 -*-


from django.db import models

from check_system.models.models import CheckSystemOs

class Tpl(models.Model):
    """
    模板
    """
    tpl_name = models.CharField(max_length=20, default="", verbose_name="模板名称")
    tpl_os = models.CharField(max_length=20, default="", verbose_name="巡检对象")
    author = models.CharField(max_length=200,default="",null=True, verbose_name="作者")
    description = models.CharField(max_length=1000, default="", verbose_name="模板描述")
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = "模板"
        verbose_name_plural = verbose_name

    def to_dict(self):
        return {
            "id": self.id,
            "tpl_name": self.tpl_name,
            "tpl_os": self.tpl_os,
            "tpl_os_name": self.get_os_name(),
            "author": self.author,
            "description": self.description,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_time": self.updated_time.strftime("%Y-%m-%d %H:%M:%S"),
            "related_task": [task for task in self.task_set.filter(is_deleted=0).values('task_name')],
        }

    def to_dict_log(self):
        return {
            "tpl_name": self.tpl_name,
            "tpl_os": self.tpl_os,
            "description": self.description,
            "author": self.author,
        }

    def to_dict_name(self):
        return {
            "id": self.id,
            "tpl_name": self.tpl_name,
        }

    def get_os_name(self):
        os_obj = CheckSystemOs.objects.get(pk=self.tpl_os)
        return os_obj.os_name
