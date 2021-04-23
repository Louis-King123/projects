# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


class BkUser(models.Model):
    user_name = models.CharField(max_length=50, verbose_name='蓝鲸用户组名称')
    user_id = models.IntegerField(null=True, verbose_name='蓝鲸用户ID')
    class Meta:
        db_table = 'check_system_bk_user'

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "user_id": self.user_id,
        }
