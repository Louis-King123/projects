# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Base(models.Model):
    # 是否删除
    # 1 已删除 0 未删除
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        abstract = True


class CheckSystemOs(models.Model):
    os_name = models.CharField(max_length=20, blank=True, null=True)
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'check_system_os'

    def to_dict(self):
        return {
            "id": self.id,
            "os_name": self.os_name,
            "is_deleted": self.is_deleted,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_time": self.updated_time.strftime("%Y-%m-%d %H:%M:%S")
        }


class CheckSystemTplQuta(models.Model):
    tpl_id = models.PositiveIntegerField(verbose_name='模板ID')
    quota_id = models.PositiveIntegerField(verbose_name='脚本ID')
    quota_threshold = models.CharField(max_length=200, verbose_name='比较条件')
    is_deleted = models.PositiveIntegerField(default=0, null=True, verbose_name='是否删除')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'check_system_tpl_quota'

    def to_dict(self):
        return {
            "tpl_id": self.tpl_id,
            "quota_id": self.quota_id,
            "quota_threshold": self.quota_threshold,
        }

    def to_dict_log(self):
        return {
            "id": self.quota_id,
            "quota_threshold": self.quota_threshold,
        }


class SystemConfig(Base):
    config_type = models.CharField(max_length=60,default='', verbose_name="配置类型")
    config_value = models.CharField(max_length=60,default='', verbose_name="值")
    description = models.TextField(blank=True,null=True,default='', verbose_name="描述(预留)")

    class Meta:
        db_table = 'check_system_config'
