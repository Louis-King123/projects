# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# 机房情况
class MachineRoom(models.Model):
    sJorgCode = models.CharField(db_column='sJorgCode', max_length=12)  # Field name made lowercase.
    sJrmName = models.CharField(db_column='sJrmName', max_length=50)  # Field name made lowercase.
    sJrmCode = models.CharField(db_column='sJrmCode', max_length=50)  # Field name made lowercase.
    sJrmPosition = models.CharField(db_column='sJrmPosition', max_length=100)  # Field name made lowercase.
    sJcabCount = models.CharField(db_column='sJcabCount', max_length=20)  # Field name made lowercase.
    sJcabInstalled = models.CharField(db_column='sJcabInstalled', max_length=20)  # Field name made lowercase.
    sJsdTotalCapacity = models.CharField(db_column='sJsdTotalCapacity', max_length=20)  # Field name made lowercase.
    sJupsCapacity = models.CharField(db_column='sJupsCapacity', max_length=20)  # Field name made lowercase.
    sJairCount = models.CharField(db_column='sJairCount', max_length=20)  # Field name made lowercase.
    sJisTHmon = models.CharField(db_column='sJisTHmon', max_length=2)  # Field name made lowercase.
    sJisWatermon = models.CharField(db_column='sJisWatermon', max_length=2)  # Field name made lowercase.
    sJisFiremon = models.CharField(db_column='sJisFiremon', max_length=2)  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'machine_room'


# 基础软件实例
class BaseSoftData(models.Model):
    sJorgCode = models.CharField(db_column='sJorgCode', max_length=12)  # Field name made lowercase.
    sJsoftType = models.PositiveIntegerField(db_column='sJsoftType')  # Field name made lowercase.
    sJsoftName = models.CharField(db_column='sJsoftName', max_length=50)  # Field name made lowercase.
    sJsoftVersion = models.CharField(db_column='sJsoftVersion', max_length=50)  # Field name made lowercase.
    sJsoftIp = models.CharField(db_column='sJsoftIp', max_length=50)  # Field name made lowercase.
    sJsoftPort = models.CharField(db_column='sJsoftPort', max_length=50)  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'base_soft_data'


# 云平台总体建设
class CloudDataAll(models.Model):
    sJorgCode = models.CharField(db_column='sJorgCode', max_length=12)  # Field name made lowercase.
    sJvmPlatCode = models.CharField(db_column='sJvmPlatCode', max_length=200)  # Field name made lowercase.
    sJcloudBrand = models.CharField(db_column='sJcloudBrand', max_length=200)  # Field name made lowercase.
    sJcloudScale = models.PositiveIntegerField(db_column='sJcloudScale')  # Field name made lowercase.
    sJcloudServCount = models.PositiveIntegerField(db_column='sJcloudServCount')  # Field name made lowercase.
    sJcloudServTypes = models.CharField(db_column='sJcloudServTypes', max_length=255)  # Field name made lowercase.
    sJcloudAppCount = models.PositiveIntegerField(db_column='sJcloudAppCount')  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cloud_data_all'


# 云平台分服务类型建设
class CloudServeType(models.Model):
    sJorgCode = models.CharField(db_column='sJorgCode', max_length=12)  # Field name made lowercase.
    sJcloudServType = models.CharField(db_column='sJcloudServType', max_length=50)  # Field name made lowercase.
    sJcloudServName = models.CharField(db_column='sJcloudServName', max_length=200)  # Field name made lowercase.
    sJcloudServCode = models.CharField(db_column='sJcloudServCode', max_length=100)  # Field name made lowercase.
    sJcloudcount = models.PositiveIntegerField(db_column='sJcloudcount')  # Field name made lowercase.
    sJcloudBrandCpu = models.PositiveIntegerField(db_column='sJcloudBrandCpu')  # Field name made lowercase.
    sJcloudBrandMem = models.PositiveIntegerField(db_column='sJcloudBrandMem')  # Field name made lowercase.
    sJcloudBrandStore = models.PositiveIntegerField(db_column='sJcloudBrandStore')  # Field name made lowercase.
    sJcloudBrandBand = models.PositiveIntegerField(db_column='sJcloudBrandBand')  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cloud_serve_type'


class OrgCode(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'org_code'


# 机房环境运行指标数据
class PcRoomData(models.Model):
    orgCode = models.CharField(db_column='orgCode', max_length=12)  # Field name made lowercase.
    rmCode = models.CharField(db_column='rmCode', max_length=12)  # Field name made lowercase.
    envHealthValue = models.CharField(db_column='envHealthValue', max_length=50)  # Field name made lowercase.
    powerHealthValue = models.CharField(db_column='powerHealthValue', max_length=50)  # Field name made lowercase.
    electrRealPower = models.CharField(db_column='electrRealPower', max_length=50)  # Field name made lowercase.
    upsRealPower = models.CharField(db_column='upsRealPower', max_length=50)  # Field name made lowercase.
    roomAverTemp = models.CharField(db_column='roomAverTemp', max_length=50)  # Field name made lowercase.
    roomAverHum = models.CharField(db_column='roomAverHum', max_length=50)  # Field name made lowercase.
    waterLeakStatus = models.CharField(db_column='waterLeakStatus', max_length=50)  # Field name made lowercase.
    fireStatus = models.CharField(db_column='fireStatus', max_length=50)  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pc_room_data'


# 警务微信轻应用运行监控指标
class PoliceWechatData(models.Model):
    orgCode = models.CharField(db_column='orgCode', max_length=12)  # Field name made lowercase.
    agentid = models.CharField(max_length=50)
    appName = models.CharField(db_column='appName', max_length=50)  # Field name made lowercase.
    checkTime = models.CharField(db_column='checkTime', max_length=50)  # Field name made lowercase.
    result = models.PositiveIntegerField()
    expdesc = models.CharField(max_length=255, blank=True, null=True)
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'police_wechat_data'


# 上报记录
class ReportLog(models.Model):
    reportType = models.PositiveIntegerField(db_column='reportType')  # Field name made lowercase.
    requestData = models.TextField(db_column='requestData', blank=True, null=True)  # Field name made lowercase.
    resultData = models.TextField(db_column='resultData', blank=True,null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'report_log'


# 服务器监测指标
class ServerData(models.Model):
    orgCode = models.CharField(db_column='orgCode', max_length=12)  # Field name made lowercase.
    ciId = models.CharField(db_column='ciId', max_length=50)  # Field name made lowercase.
    devOnlineState = models.CharField(db_column='devOnlineState', max_length=50)  # Field name made lowercase.
    devResponseTime = models.PositiveIntegerField(db_column='devResponseTime')  # Field name made lowercase.
    devAlertLevel = models.PositiveIntegerField(db_column='devAlertLevel')  # Field name made lowercase.
    devCpuRate = models.CharField(db_column='devCpuRate', max_length=50)  # Field name made lowercase.
    devMemRate = models.CharField(db_column='devMemRate', max_length=50)  # Field name made lowercase.
    devDiskRate = models.CharField(db_column='devDiskRate', max_length=50)  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'server_data'


# 服务器监测总体情况
class ServerDataAll(models.Model):
    orgCode = models.CharField(db_column='orgCode', max_length=12)  # Field name made lowercase.
    devHealthValue = models.CharField(db_column='devHealthValue', max_length=50)  # Field name made lowercase.
    devOnlineRate = models.CharField(db_column='devOnlineRate', max_length=50)  # Field name made lowercase.
    devAverCpuRate = models.CharField(db_column='devAverCpuRate', max_length=50)  # Field name made lowercase.
    devAverMemRate = models.CharField(db_column='devAverMemRate', max_length=50)  # Field name made lowercase.
    devAverDiskRate = models.CharField(db_column='devAverDiskRate', max_length=50)  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'server_data_all'


# 软件实例运行指标
class SoftData(models.Model):
    orgCode = models.CharField(db_column='orgCode', max_length=12)  # Field name made lowercase.
    ciId = models.CharField(db_column='ciId', max_length=50)  # Field name made lowercase.
    runningState = models.CharField(db_column='runningState', max_length=50)  # Field name made lowercase.
    tcpState = models.CharField(db_column='tcpState', max_length=50)  # Field name made lowercase.
    webResponseTime = models.PositiveIntegerField(db_column='webResponseTime')  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'soft_data'


# 故障告警数据
class FaultAlert(models.Model):
    orgCode = models.CharField(db_column='orgCode', max_length=12)  # Field name made lowercase.
    alertId = models.CharField(db_column='alertId', max_length=50)  # Field name made lowercase.
    name = models.CharField(max_length=50)
    severity = models.CharField(max_length=1)
    description = models.CharField(max_length=200)
    entityName = models.CharField(db_column='entityName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    entityAddr = models.CharField(db_column='entityAddr', max_length=15, blank=True, null=True)  # Field name made lowercase.
    firstTime = models.DateTimeField(db_column='firstTime')  # Field name made lowercase.
    lastTime = models.DateTimeField(db_column='lastTime')  # Field name made lowercase.
    properties = models.TextField(blank=True, null=True)
    ciId = models.CharField(db_column='ciId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    proStatus = models.CharField(db_column='proStatus', max_length=2)  # Field name made lowercase.
    orderNo = models.CharField(db_column='orderNo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isReported = models.PositiveIntegerField(db_column='isReported')  # Field name made lowercase.
    isDeleted = models.IntegerField(db_column='isDeleted')  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime')  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fault_alert'