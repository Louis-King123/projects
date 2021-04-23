 # -*- coding: utf-8 -*-


from django.db import models
from check_system.models.models import CheckSystemOs
from check_system.models.models import CheckSystemTplQuta
from check_system.models.tpl import Tpl

class Quota(models.Model):
    """
    模板
    """
    quota_name = models.CharField(max_length=40, default="", verbose_name="指标名称")
    quota_tag = models.CharField(max_length=40, default="")
    quota_os = models.CharField(max_length=20, default="", verbose_name="指标对应的操作系统")
    quota_class=models.CharField(max_length=20, default="", verbose_name="指标所属分类")
    quota_handler = models.CharField(max_length=200, default="", verbose_name="日志处理工具")
    quota_threshold = models.CharField(max_length=200, default="", verbose_name="报警阈值")
    script_type = models.IntegerField(default=0, verbose_name="脚本类型(shell ps bat python)")
    script_content = models.TextField(max_length=10000, default="", verbose_name="脚本内容")
    is_required = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=200,default="admin",null=True,verbose_name="作者")
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        managed = False
        verbose_name = "自定义巡检项"
        verbose_name_plural = verbose_name

    def to_dict(self):
        os_name = "Linux通用"
        if int(self.quota_os) != 99:
            os_name = CheckSystemOs.objects.get(pk=self.quota_os).os_name
        return {
            "id": self.id,
            "quota_name": self.quota_name,
            "quota_os":os_name,
            "quota_os_id":self.quota_os,
            "quota_handler": self.quota_handler,
            "quota_threshold": self.quota_threshold,
            "script_type": self.script_type,
            "script_content": self.script_content,
            "is_required": self.is_required,
            "author": self.author,
            "quota_class_id": self.quota_class,
            "related_tpl" : self.related_tpl()
        }

    def to_dict_onshow(self):
        return {
            "id": f"{self.quota_class}-{self.id}",
            "quota_name": self.quota_name,
            "quota_os": self.quota_os,
            "quota_handler": self.quota_handler,
            "quota_threshold": self.quota_threshold,
            "quota_class_id": self.quota_class,
            "is_required": self.is_required,
        }

    def to_dict_log(self):
        return {
            "quota_name": self.quota_name,
            "quota_os": CheckSystemOs.objects.get(pk=self.quota_os).os_name,
            "script_type": self.script_type,
            "script_content": self.script_content,
            "quota_handler": self.quota_handler,
            "quota_threshold": self.quota_threshold,
            "quota_class": "自定义巡检",
            "author": self.author,
        }

    def related_tpl(self):
        tpl_quotas = [tpl_quota.to_dict() for tpl_quota in CheckSystemTplQuta.objects.filter(quota_id=self.id, is_deleted=0)]
        tpl_ids = [tpl["tpl_id"] for tpl in tpl_quotas]
        return [tpl.to_dict_name() for tpl in Tpl.objects.filter(id__in=tpl_ids).all()]