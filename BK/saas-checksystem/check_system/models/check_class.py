# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CheckSystemClass(models.Model):
    class_name = models.CharField(max_length=128)
    sort = models.PositiveIntegerField(default=0)
    is_deleted = models.IntegerField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'check_system_class'

    def to_dict(self):
        return {
            "id": self.id,
            "class_name": self.class_name,
            "is_deleted": self.is_deleted,
            "created_time": self.created_time,
            "updated_time": self.updated_time,
        }




