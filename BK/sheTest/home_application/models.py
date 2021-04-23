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


class History(models.Model):
    biz_id = models.IntegerField(verbose_name="业务ID")
    tmp_id = models.IntegerField(verbose_name="模版ID")
    inst_id = models.CharField(max_length=128, verbose_name="作业ID")
    inst_status = models.IntegerField(default=1, verbose_name="作业状态")
    inst_finish = models.BooleanField(default=False, verbose_name="是否完成")
    log_id = models.CharField(max_length=128, null=True, blank=True, verbose_name="日志")
    created_time = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')

    def to_dict(self):
        return {
            "id": self.id,
            "biz_id": self.biz_id,
            "tmp_id": self.tmp_id,
            "inst_id": self.inst_id,
            "inst_status": self.inst_status,
            "inst_finish": self.inst_finish,
            "log_id": self.log_id,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Logs(models.Model):
    custom_id = models.CharField(max_length=128, null=True, blank=True, verbose_name="自定义ID")
    ip = models.CharField(max_length=32, verbose_name="ip")
    content = models.CharField(max_length=2048, verbose_name="执行结果")

    def to_dict(self):
        return {
            "ip": self.ip,
            "content": self.content,
            "id": self.id,
            "custom_id": self.custom_id
        }