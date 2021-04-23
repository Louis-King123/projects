# -*- coding: utf-8 -*-

import random
import uuid

from django.utils import timezone

from app.models import CloudDataAll, PcRoomData, ServerData, ServerDataAll, SoftData, PoliceWechatData, BaseSoftData, \
    CloudServeType, FaultAlert, MachineRoom


class Generator:

    orgCode = '310117000000'

    @staticmethod
    def create_pc_room_data():
        """
        机房运行环境指标
        """
        room_aver_temp = random.randint(20, 25)
        room_aver_hum = random.randint(40, 55)
        room_data = [{
                'orgCode': str(Generator.orgCode),
                'rmCode': str(Generator.orgCode),
                'envHealthValue': str(random.randint(90, 100)),
                'powerHealthValue': str(random.randint(90, 100)),
                'electrRealPower': str(random.choice([1000, 1500, 2000, 2500, 3000])),
                'upsRealPower': str(random.choice([600, 800, 1000, 1100, 1200])),
                'roomAverTemp': str(room_aver_temp),
                'roomAverHum': str(room_aver_hum),
                'waterLeakStatus': str(10),
                'fireStatus': str(10),
                'isReported': 0,
                'isDeleted': 0,
                'createdTime': timezone.now(),
                'updatedTime': timezone.now()
            }, {
                'orgCode': str(Generator.orgCode),
                'rmCode': str(Generator.orgCode),
                'envHealthValue': str(random.randint(90, 100)),
                'powerHealthValue': str(random.randint(90, 100)),
                'electrRealPower': str(random.choice([1000, 1500, 2000, 2500, 3000])),
                'upsRealPower': str(random.choice([600, 800, 1000, 1100, 1200])),
                'roomAverTemp': str(room_aver_temp),
                'roomAverHum': str(room_aver_hum),
                'waterLeakStatus': str(10),
                'fireStatus': str(10),
                'isReported': 0,
                'isDeleted': 0,
                'createdTime': timezone.now(),
                'updatedTime': timezone.now()
            }]
        query_set_list = []
        for data in room_data:
            query_set_list.append(PcRoomData(**data))
        PcRoomData.objects.bulk_create(query_set_list)

    @staticmethod
    def create_base_soft_data():
        """
        基础软件实例
        """
        soft_data = [{
            'type': 1,
            'value': [{
                'name': 'mysql',
                'version': ['5.6.0', '5.7.1', '5.8.1'],
                'port': 3306
            }, {
                'name': 'sqlserver',
                'version': [2017, 2016, 2014, 2012],
                'port': 1433
            }, {
                'name': 'sqllite',
                'version': ['3.15.1', '3.25.8', '3.11.4'],
                'port': ''
            }, {
                'name': 'oracle',
                'version': ['11.1', '11.2', '12.1', '12.2'],
                'port': 1512
            }, {
                'name': 'mongo',
                'version': ['4.0.2', '4.0.8', '4.0.4'],
                'port': 27017
            }, {
                'name': 'redis',
                'version': ['5.11.2', '5.15.8', '5.11.4'],
                'port': 6379
            }]
        }, {
            'type': 2,
            'value': [{
                'name': 'rabbit mq',
                'version': ['3.6.3', '3.7.1', '3.7.6'],
                'port': 25672
            }, {
                'name': 'kafka',
                'version': ['0.9.2.2', '0.8.1.1', '0.10.0.0'],
                'port': 9092,
            }, {
                'name': 'tomcat',
                'version': ['9.0', '8.0'],
                'port': 8888,
            }, {
                'name': 'nginx',
                'version': ['1.12.1', '1.6.2', '1.18.3'],
                'port': 443,
            }]
        }, {
            'type': 9,
            'value': [{
                'name': 'python',
                'version': ['3.6.8', '3.8.5', '3.6.5'],
                'port': 8000,
            }, {
                'name': 'go',
                'version': ['1.1', '1.2', '1.14', '1.13', '1.12'],
                'port': 8080,
            }, {
                'name': 'php',
                'version': ['5.4.24', '5.6.11', '7.1.13', '7.2.4', '7.3.15'],
                'port': 8081,
            }, {
                'name': 'node',
                'version': ['8.6.5', '12.15.4', '14.15.1'],
                'port': 3000,
            }, {
                'name': 'git',
                'version': ['2.1.0', '2.1.1'],
                'port': 8181,
            }]
        }]
        count = 0
        base_soft_data = []
        while count <= 20:
            base_soft = random.choice(soft_data)
            soft_name = random.choice(base_soft.get('value'))
            base_soft_data.append({
                'sJorgCode': str(Generator.orgCode),
                'sJsoftType': str(base_soft.get('type')),
                'sJsoftName': soft_name.get('name'),
                'sJsoftVersion': random.choice(soft_name.get('version')),
                'sJsoftIp': '15.208.17.' + str(random.randint(5, 254)),
                'sJsoftPort': str(soft_name.get('port')),
                'isReported': 0,
                'isDeleted': 0,
                'createdTime': timezone.now(),
                'updatedTime': timezone.now(),
            })
            count += 1
        query_set_list = []
        for data in base_soft_data:
            query_set_list.append(BaseSoftData(**data))
        BaseSoftData.objects.bulk_create(query_set_list)

    @staticmethod
    def create_cloud_data_all():
        """
        云平台总体建设
        """
        cloud_data = {
            'sJorgCode': Generator.orgCode,
            'sJvmPlatCode': 'cn-shanghai-sjfj-am1590001-a',
            'sJcloudBrand': '阿里云',
            'sJcloudScale': str(140),
            'sJcloudServCount': str(6),
            'sJcloudServTypes': 'ECS,OSS,VPC,SLB,数据库,大数据',
            'sJcloudAppCount': str(6),
            'createdTime': timezone.now(),
            'isReported': 0,
            'isDeleted': 0,
            'updatedTime': timezone.now()
        }
        CloudDataAll.objects.create(**cloud_data)

    @staticmethod
    def create_server_data():
        """
        服务器监测指标
        """
        count = 0
        server_data = []
        while count <= 58:
            ci_id = str(uuid.uuid4()).replace('-', '')
            dev_online_state = [10, 20]
            server_data.append({
                'orgCode': str(Generator.orgCode),
                'ciId': ci_id,
                'devOnlineState': str(dev_online_state[0]) if random.randint(1, 10) > 3 else str(dev_online_state[1]),
                'devResponseTime': str(random.randint(20, 500)),
                'devAlertLevel': str(random.randint(0, 3)),
                'devCpuRate': str(random.randint(3, 40)),
                'devMemRate': str(random.randint(40, 50)),
                'devDiskRate': str(random.randint(10, 30)),
                'isReported': 0,
                'isDeleted': 0,
                'createdTime': timezone.now(),
                'updatedTime': timezone.now()
            })
            count += 1
        query_set_list = []
        server_data_all = {
            'orgCode': str(Generator.orgCode),
            'devHealthValue': str(random.randint(85, 100)),
            'devOnlineRate': str(random.randint(93, 95)),
            'isReported': 0,
            'isDeleted': 0,
            'createdTime': timezone.now(),
            'updatedTime': timezone.now(),
        }
        dev_aver_cpu_total = 0
        dev_aver_disk_total = 0
        dev_aver_mem_total = 0
        for data in server_data:
            query_set_list.append(ServerData(**data))
            dev_aver_cpu_total += data.get('devCpuRate')
            dev_aver_mem_total += data.get('devMemRate')
            dev_aver_disk_total += data.get('devDiskRate')

        ServerData.objects.bulk_create(query_set_list)
        server_data_all.update({
            'devAverCpuRate': str(round(dev_aver_cpu_total / count, 0)),
            'devAverMemRate': str(round(dev_aver_mem_total / count, 0)),
            'devAverDiskRate': str(round(dev_aver_disk_total / count, 0)),
        })
        ServerDataAll.objects.create(**server_data_all)

    @staticmethod
    def create_soft_data():
        """
        软件运行指标
        """
        count = 0
        soft_data = []
        while count <= 59:
            tcp_state = [10, 20]
            ci_id = str(uuid.uuid4()).replace('-', '')
            soft_data.append({
                'orgCode': str(Generator.orgCode),
                'ciId': ci_id,
                'runningState': str(tcp_state[0]) if random.randint(1, 10) > 3 else str(tcp_state[1]),
                'tcpState': str(tcp_state[0]) if random.randint(1, 10) > 3 else str(tcp_state[1]),
                'webResponseTime': str(random.randint(20, 665)),
                'isReported': 0,
                'isDeleted': 0,
                'createdTime': timezone.now(),
                'updatedTime': timezone.now()
            })
            count += 1
        query_set_list = []
        for data in soft_data:
            query_set_list.append(SoftData(**data))

        SoftData.objects.bulk_create(query_set_list)

    @staticmethod
    def create_police_wechat_data():
        """
        警务微信运行指标
        """
        police_wechat_data = {
            'orgCode': str(Generator.orgCode),
            'agentid': str(uuid.uuid4()).replace('-', ''),
            'appName': '警务轻应用' + str(random.randint(1, 100)),
            'checkTime': timezone.now(),
            'result': str(10) if random.randint(1, 10) > 3 else str(20),
            'expdesc': "无",
            'isReported': 0,
            'isDeleted': 0,
            'createdTime': timezone.now(),
            'updatedTime': timezone.now()
        }
        PoliceWechatData.objects.create(**police_wechat_data)

    @staticmethod
    def create_cloud_server_type():
        """
        云平台服务类型
        """
        cloud_server_types = {
            'rds' : [{
                'analyticdb': 14
            }, {
                'mysql': 12
            }],
            'oss': [{
                'OssHybridCluster': 10
            }],
            'tianji': [{
                'taiji': 22
            }],
            'ecs': [{
                'ECS-CPU-A-fde1': 17
            }, {
                'ECS-IO11-A-fde3': 6
            }, {
                'ECS-IO8River-A-fde2': 10
            }],
            'odps': [{
                'HybridOdpsCluster-A-20201221-fdb6': 12
            }],
            'datahub': [{
                'DataHubCluster-A-20201221-fda3': 4
            }],
            'slb': [{
                'slbCluster-A-20201221-fda1': 6
            }],
            'mq': [{
                'mq': 0
            }]
        }
        server_data = []
        for data in cloud_server_types:
            for info in cloud_server_types.get(data):
                key = list(info.keys())
                value = list(info.values())
                app_count = random.randint(10, 30)
                server_data.append({
                    'sJorgCode': str(Generator.orgCode),
                    'sJcloudServType': str(data),
                    'sJcloudServName': str(key[0]),
                    'sJcloudServCode': str(value[0]),
                    'sJcloudcount': str(app_count),
                    'sJcloudBrandCpu': str(2**random.randint(3, 6)),
                    'sJcloudBrandMem': str(2**random.randint(3, 6)),
                    'sJcloudBrandStore': random.choice([item for item in range(1000) if item >= 50 and item % 10 == 0]),
                    'sJcloudBrandBand': str(random.choice([5, 10, 100, 200, 1000])),
                    'isReported': 0,
                    'isDeleted': 0,
                    'createdTime': timezone.now(),
                    'updatedTime': timezone.now()
                })
        query_set_list = []
        for data in server_data:
            query_set_list.append(CloudServeType(**data))

        CloudServeType.objects.bulk_create(query_set_list)

    @staticmethod
    def machine_room():
        """
        机房情况
        """
        machine_room_data = {
            'sJorgCode': str(Generator.orgCode),
            'sJrmName': random.choice(['三楼核心机房', '三楼网安机房']),
            'sJrmCode': str(uuid.uuid4()).replace('-', ''),
            'sJrmPosition': random.choice(['一号机房', '二号机房', '三号机房']),
            'sJcabCount': str(random.randint(180, 200)),
            'sJcabInstalled': str(random.randint(100, 180)),
            'sJsdTotalCapacity': '50000',
            'sJupsCapacity': '50000',
            'sJairCount': str(random.choice([30, 40, 41, 45])),
            'sJisTHmon': str(random.choice([10, 20])),
            'sJisWatermon': str(random.choice([10, 20])),
            'sJisFiremon': str(random.choice([10, 20])),
            'isReported': 0,
            'isDeleted': 0,
            'createdTime': timezone.now(),
            'updatedTime': timezone.now(),
        }
        MachineRoom.objects.create(**machine_room_data)

    @staticmethod
    def fault_alert():
        """
        故障告警数据
        """
        count = 0
        fault_alert_data = []
        while count <= 25:
            addr = '192.168.1.' + str(random.randint(5, 254))
            fault_alert_data.append({
                'orgCode': str(Generator.orgCode),
                'alertId': str(uuid.uuid4()).replace('-', ''),
                'name': '15.208.17.' + str(random.randint(5, 254)) + '-服务器离线',
                'severity': str(random.randint(0, 3)),
                'description': '网络设备不可达通知',
                'entityName': addr + '-host' + addr.replace('-', ''),
                'entityAddr': addr,
                'firstTime': timezone.now(),
                'lastTime': timezone.now(),
                'properties': '',
                'ciId': str(uuid.uuid4()).replace('-', ''),
                'proStatus': str(random.choice([10, 20, 30])),
                'orderNo': str(uuid.uuid4()).replace('-', ''),
                'isReported': 0,
                'isDeleted': 0,
                'createdTime': timezone.now(),
                'updatedTime': timezone.now(),
            })
            count += 1
        query_set_list = []
        for data in fault_alert_data:
            query_set_list.append(FaultAlert(**data))

        FaultAlert.objects.bulk_create(query_set_list)


