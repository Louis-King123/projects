# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

# from django.db import models

# Create your models here.
from django.db import models
import datetime


class BackupHistory(models.Model):
    ip = models.CharField(max_length=32, verbose_name="IP")
    file_list = models.TextField(null=True, blank=True, verbose_name="文件列表")
    file_count = models.IntegerField(default=0, verbose_name="文件数量")
    file_size = models.CharField(max_length=32, default="0", verbose_name="文件大小")
    backup_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="备份时间")
    backup_person = models.CharField(max_length=32, verbose_name="备份人")
    job_link = models.TextField(null=True, blank=True, verbose_name="JOB链接")

    def to_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "file_list": self.file_list,
            "file_count": self.file_count,
            "file_size": self.file_size,
            "backup_person": self.backup_person,
            "job_link": self.job_link,
            "backup_time": self.backup_time.strftime("%Y-%m-%d %H:%M:%S"),
        }