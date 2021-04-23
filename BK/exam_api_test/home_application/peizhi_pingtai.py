# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_request
from django.http import JsonResponse
from django.conf import settings
from blueking.component.client import ComponentClient


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt

# ###########  配置平台 ##############
class ConfigPlatform(object):

    @classmethod
    def create_business(cls, request):
        """新建业务"""
        bk_app_code = settings.APP_CODE
        bk_app_secret = settings.SECRET_KEY
        bk_token = request.COOKIES['bk_token']  # bk_token

        # 获取client方法1
        # client = get_client_by_request(request)

        # 获取client方法2
        client = ComponentClient(
            bk_app_code=bk_app_code,
            bk_app_secret=bk_app_secret,
            common_args={'bk_token': bk_token}
        )

        kwargs = {
            "bk_supplier_account": "0",
            "data": {
                "bk_biz_name": "cc_app_test",
                "bk_biz_maintainer": "admin",
                "bk_biz_productor": "admin",
                "bk_biz_developer": "admin",
                "bk_biz_tester": "admin",
                "time_zone": "Asia/Shanghai",
                "language": "1"
            }
        }

        info = client.cc.create_business(kwargs)
        return JsonResponse(info)

    @classmethod
    def search_business(cls, request):
        """
        查询业务
        result: 2/蓝鲸，5/自动巡检 ......
        """
        client = get_client_by_request(request)

        kwargs = {
            # "fields": [
            #     "bk_biz_id",
            #     "bk_biz_name"
            # ],
            "page": {
                "start": 0,
                "limit": 10,
                "sort": ""
            }
        }

        info = client.cc.search_business(kwargs)

        alls = info['data']['info']
        for app in alls:
            print(app['bk_biz_id'])
            print(app['bk_biz_name'])
            print('*' * 30)
        """
        所有字段
        "bk_biz_id": 2, 
        "language": "1", 
        "life_cycle": "2", 
        "bk_biz_developer": "", 
        "bk_biz_maintainer": "admin", 
        "bk_biz_tester": "", 
        "time_zone": "Asia/Shanghai", 
        "default": 0, 
        "create_time": "2021-01-06T11:29:13.993+08:00", 
        "bk_biz_productor": "", 
        "bk_supplier_account": "0", 
        "operator": "", 
        "bk_biz_name": "\u84dd\u9cb8", 
        "last_time": "2021-01-06T11:29:13.993+08:00"
        """
        return JsonResponse(info)

    @classmethod
    def search_biz_inst_topo(cls, request):
        """查询业务实例拓扑
            根据业务id获取拓扑关系，该接口包括，集群信息，模块信息
            参数：biz_id 业务ID
        """
        biz_id = request.GET.get('biz_id', 2)
        # biz_id = 2  # 测试默认
        kwargs = {'bk_biz_id': biz_id}
        client = get_client_by_request(request)
        info = client.cc.search_biz_inst_topo(kwargs)

        result_topo_list = []
        for topo in info['data']:
            biz_dict = {
                'name': topo['bk_inst_name'],
                'expanded': True,
                'bk_obj_id': 'biz',
                'id': biz_id
            }
            set_child = []
            for op in topo['child']:
                if len(op['child']):
                    model_child = []
                    for mo in op['child']:
                        model_child.append(
                            {'name': mo['bk_inst_name'], 'id': mo['bk_inst_id'], 'bk_obj_id': mo['bk_obj_id']})
                    set_child.append({'name': op['bk_inst_name'], 'id': op['bk_inst_id'], 'expanded': False,
                                      'children': model_child, 'bk_obj_id': op['bk_obj_id']})
                else:
                    set_child.append({'name': op['bk_inst_name'], 'id': op['bk_inst_id'], 'bk_obj_id': op['bk_obj_id']})
            biz_dict['children'] = set_child
            result_topo_list.append(biz_dict)

        return JsonResponse({"data": result_topo_list})
        # return JsonResponse(info)

    @classmethod
    def search_biz_set(cls, request):
        """
            根据业务id获取集群信息
            参数：biz_id 业务ID
        """
        biz_id = request.GET.get('biz_id', 2)
        # biz_id = 2  # 测试默认
        kwargs = {'bk_biz_id': biz_id}
        client = get_client_by_request(request)
        info = client.cc.search_biz_inst_topo(kwargs)

        result_list = []
        for topo in info['data']:
            for op in topo['child']:
                result_list.append({'name': op['bk_inst_name'], 'id': op['bk_inst_id'], 'bk_obj_id': op['bk_obj_id']})

        return JsonResponse({"data": result_list})

    @classmethod
    def search_biz_set_module(cls, request):
        """
            根据业务id 集群id 获取模块信息
            参数：biz_id 业务ID
        """
        biz_id = request.GET.get('biz_id', 2)
        set_id = request.GET.get('set_id', 4)
        # biz_id = 2  # 测试默认
        kwargs = {'bk_biz_id': biz_id}
        client = get_client_by_request(request)
        info = client.cc.search_biz_inst_topo(kwargs)

        result_list = []
        for topo in info['data']:
            for op in topo['child']:
                if op.get('bk_inst_id', '') and int(op['bk_inst_id']) == set_id:
                    if len(op['child']):
                        for mo in op['child']:
                            result_list.append(
                                {'name': mo['bk_inst_name'], 'id': mo['bk_inst_id'], 'bk_obj_id': mo['bk_obj_id']})

        return JsonResponse({"data": result_list})

    # ==================
    @classmethod
    def list_biz_hosts(cls, request):
        """查询业务下的主机
        根据业务 ID 查询业务下的主机，可附带其他的过滤信息，如集群 id 多个用逗号隔开,模块 id 多个用逗号隔开
        """
        client = get_client_by_request(request)
        biz_id = request.GET.get('bk_biz_id', 2)
        set_id = request.GET.get('bk_set_ids', '4')
        module_id = request.GET.get('bk_module_ids', '12')

        kwargs = {"page": {
                    "start": 0,
                    "limit": 10,
                    "sort": "bk_host_id"
                },
                "fields": [
                    "bk_host_id",
                    "bk_cloud_id",
                    "bk_host_innerip",
                    "bk_os_type",
                    "bk_mac"
                ],
                'bk_biz_id': biz_id}
        # if set_id: kwargs['bk_set_ids'] = [int(i) for i in set_id.split(',')]
        # if module_id: kwargs['bk_module_ids'] = [int(i) for i in module_id.split(',')]

        info = client.cc.list_biz_hosts(kwargs)

        """
            所有字段
            bk_isp_name	string	所属运营商	0:其它；1:电信；2:联通；3:移动
            bk_sn	string	设备 SN	
            operator	string	主要维护人	
            bk_outer_mac	string	外网 MAC	
            bk_state_name	string	所在国家	CN:中国，详细值，请参考 CMDB 页面
            bk_province_name	string	所在省份	
            import_from	string	录入方式	1:excel;2:agent;3:api
            bk_sla	string	SLA 级别	1:L1;2:L2;3:L3
            bk_service_term	int	质保年限	1-10
            bk_os_type	string	操作系统类型	1:Linux;2:Windows;3:AIX
            bk_os_version	string	操作系统版本	
            bk_os_bit	int	操作系统位数	
            bk_mem	string	内存容量	
            bk_mac	string	内网 MAC 地址	
            bk_host_outerip	string	外网 IP	
            bk_host_name	string	主机名称	
            bk_host_innerip	string	内网 IP	
            bk_host_id	int	主机 ID	
            bk_disk	int	磁盘容量	
            bk_cpu_module	string	CPU 型号	
            bk_cpu_mhz	int	CPU 频率	
            bk_cpu	int	CPU 逻辑核心数	1-1000000
            bk_comment	string	备注	
            bk_cloud_id	int	云区域	
            bk_bak_operator	string	备份维护人	
            bk_asset_id	string	固资编号
        """
        return JsonResponse({"data": info['data']['info']})

    @classmethod
    def get_host_base_info(cls, request):
        """获取主机详情"""

        client = get_client_by_request(request)
        host_id = request.GET.get('host_id')
        kwargs = {
            "bk_host_id": host_id if host_id else 3
        }

        info = client.cc.get_host_base_info(kwargs)

        """
        返回值：
        {"bk_property_value": "", "bk_property_id": "bk_bak_operator", "bk_property_name": "\u5907"}
             属性值                      属性 id                               属性名称
        """
        return JsonResponse({"data": info['data']})
    # =====================

    # =====================
    @classmethod
    def list_service_template(cls, request):
        """根据业务 id 查询服务模板列表,可加上服务分类 id 进一步查询"""

        client = get_client_by_request(request)
        biz_id = request.GET.get('biz_id', 2)
        service_category_id = request.GET.get('service_category_id', '')
        kwargs = {
            "bk_biz_id": biz_id
            # 'service_category_id': service_category_id
        }

        info = client.cc.list_service_template(kwargs)
        return JsonResponse({"data": info['data']})

    @classmethod
    def get_service_template(cls, request):
        """根据服务模板 ID 获取服务模板"""

        client = get_client_by_request(request)
        template_id = request.GET.get('template_id', 2)
        kwargs = {
            "service_template_id": template_id
        }

        info = client.cc.get_service_template(kwargs)
        return JsonResponse({"data": info['data']})

    @classmethod
    def create_service_template(cls, request):
        """根据传入的服务模板名称的服务分类 ID 创建指定名称和服务分类的服务模板"""

        client = get_client_by_request(request)
        name = request.GET.get('name')  # 服务模板名称
        service_category_id = request.GET.get('service_category_id')  # 服务分类 ID
        bk_biz_id = request.GET.get('bk_biz_id', 2)
        kwargs = {
            "bk_biz_id": 2,
            # "bk_biz_id": int(bk_biz_id),
            # "name": name,
            "name": "test_api_template2",
            "service_category_id": 21
            # "service_category_id": int(service_category_id)
        }

        info = client.cc.create_service_template(kwargs)
        return JsonResponse(info)

    @classmethod
    def update_service_template(cls, request):
        """更新服务模板 更新服务模板名称信息"""

        client = get_client_by_request(request)
        name = request.GET.get('name')  # 服务模板名称
        service_category_id = request.GET.get('service_category_id')  # 服务分类 ID
        bk_biz_id = request.GET.get('bk_biz_id', 2)
        template_id = request.GET.get('template_id', 83)  # 服务模板 ID

        kwargs = {
            "bk_biz_id": 2,
            # "bk_biz_id": int(bk_biz_id),
            # "name": name,
            "name": "test_api_template_update",
            "service_category_id": 24,  # 仅允许使用叶子结点服务分类
            # "service_category_id": int(service_category_id)
            "id": int(template_id)
        }

        info = client.cc.update_service_template(kwargs)
        return JsonResponse(info)

    @classmethod
    def delete_service_template(cls, request):
        """删除服务模板 根据服务模板 ID 删除服务模板"""

        client = get_client_by_request(request)
        bk_biz_id = request.GET.get('bk_biz_id', 2)
        template_id = request.GET.get('template_id', 84)  # 服务模板 ID

        kwargs = {
              "bk_biz_id": int(bk_biz_id),
              "service_template_id": int(template_id)
        }

        info = client.cc.delete_service_template(kwargs)
        return JsonResponse(info)
    # =====================

    @classmethod
    def find_host_biz_relations(cls, request):
        """查询主机业务关系信息 根据主机 ID 查询业务相关信息"""

        client = get_client_by_request(request)
        bk_host_id = request.GET.get('bk_host_id', '3')
        kwargs = {
            "bk_host_id": [int(i) for i in bk_host_id.split(',')]
        }

        info = client.cc.find_host_biz_relations(kwargs)
        """
        返回结果
        bk_biz_id	2
        bk_module_id	48
        bk_supplier_account	"0"
        bk_host_id	3
        bk_set_id	9
        """
        return JsonResponse({"data": info['data']})

    @classmethod
    def list_resource_pool_hosts(cls, request):
        """查询资源池中的主机  资源>主机>未分配"""

        client = get_client_by_request(request)
        kwargs = {
            "page": {
                "start": 0,
                "limit": 100,
                # "sort": "bk_host_id"
            }
        }

        info = client.cc.list_resource_pool_hosts(kwargs)
        """
        返回结果
        bk_cpu	null
        bk_isp_name	null
        bk_os_name	""
        bk_province_name	null
        bk_host_id	28
        import_from	"3"
        bk_os_version	""
        bk_disk	null
        operator	"admin"
        docker_server_version	""
        create_time	"2021-04-20T16:03:30.084+08:00"
        bk_mem	null
        bk_host_name	""
        last_time	"2021-04-20T16:03:30.084+08:00"
        bk_host_innerip	"127.0.0.1"
        bk_comment	""
        docker_client_version	""
        bk_os_bit	""
        bk_cloud_inst_id	""
        bk_outer_mac	""
        bk_state_name	null
        bk_asset_id	""
        bk_service_term	null
        bk_cloud_id	0
        bk_sla	null
        bk_cpu_mhz	null
        bk_host_outerip	""
        bk_cloud_vendor	null
        bk_cloud_host_status	null
        bk_os_type	"1"
        bk_supplier_account	"0"
        bk_mac	""
        """
        return JsonResponse({"data": info['data']})

    @classmethod
    def list_service_instance(cls, request):
        """根据业务 id 查询服务实例列表,也可以加上模块 id 等信息查询"""
        bk_biz_id = request.GET.get('bk_biz_id', 2)
        bk_module_id = request.GET.get('bk_module_id', 12)
        client = get_client_by_request(request)
        kwargs = {
            "bk_biz_id": bk_biz_id,
            "bk_module_id": bk_module_id
        }

        info = client.cc.list_service_instance(kwargs)  # 接口文档有误，bk_module_id不传获取不到实例
        """
        返回结果
        id	integer	服务实例 ID	
        name	array	服务实例名称	
        service_template_id	integer	服务模板 ID	
        bk_module_id	integer	模块 ID	
        bk_host_id	integer	主机 ID	
        """
        return JsonResponse({"data": info['data']})

    @classmethod
    def list_set_template(cls, request):
        """根据业务 id 查询集群模板"""
        bk_biz_id = request.GET.get('bk_biz_id', 2)
        # set_template_ids = request.GET.get('set_template_ids', [12])
        client = get_client_by_request(request)
        kwargs = {
            "bk_biz_id": bk_biz_id,
            # "set_template_ids": set_template_ids  # 指定模版id，则获取该id的模板信息
        }

        info = client.cc.list_set_template(kwargs)  # 接口文档有误，bk_module_id不传获取不到实例
        """
        返回结果
        id	int	集群模板 ID
        name	array	集群模板名称
        bk_biz_id	int	业务 ID
        version	int	集群模板版本
        creator	string	创建者
        modifier	string	最后修改人员
        create_time	string	创建时间
        last_time	string	更新时间
        bk_supplier_account	string	开发商账号
        """
        return JsonResponse({"data": info['data']})

    @classmethod
    def search_topo_tree(cls, request):
        """根据业务 id 查询集群模板"""
        bk_biz_id = request.GET.get('bk_biz_id', 2)
        client = get_client_by_request(request)
        kwargs = {
            "bk_biz_id": bk_biz_id
        }
        info = client.cc.search_topo_tree(kwargs)  # 接口文档有误，接口已弃用，但是文档中未删除
        return JsonResponse({"data": info['data']})

    @classmethod
    def add_host_to_resource(cls, request):
        """新增主机到资源池"""
        bk_host_innerip = request.GET.get('bk_host_innerip')
        client = get_client_by_request(request)
        kwargs = {
            "host_info": {
                "0": {
                    # "bk_host_innerip": "10.0.0.4",
                    "bk_host_innerip": bk_host_innerip,
                    "bk_cloud_id": 0,
                    "import_from": "3",
                }
            }
        }
        """
        返回参数和可设置参数
        bk_cpu	4
        bk_isp_name	null
        bk_os_name	""
        bk_province_name	null
        bk_host_id	34
        import_from	"3"
        bk_os_version	""
        bk_disk	null
        operator	""
        docker_server_version	""
        create_time	"2021-04-20T17:38:09.35+08:00"
        bk_mem	null
        bk_host_name	""
        last_time	"2021-04-20T17:38:09.35+08:00"
        bk_host_innerip	"10.0.0.4"
        bk_comment	""
        docker_client_version	""
        bk_os_bit	""
        bk_cloud_inst_id	""
        bk_outer_mac	""
        bk_state_name	null
        bk_asset_id	""
        bk_service_term	null
        bk_cloud_id	0
        bk_sla	null
        bk_cpu_mhz	null
        bk_host_outerip	""
        bk_cloud_vendor	null
        bk_cloud_host_status	null
        bk_os_type	null
        bk_supplier_account	"0"
        bk_mac	""
        bk_bak_operator	""
        bk_state	null
        bk_sn	""
        bk_cpu_module	""
        """
        info = client.cc.add_host_to_resource(kwargs)
        return JsonResponse({"data": info['data']})

    @classmethod
    def delete_host(cls, request):
        """删除主机  主机 id，多个以逗号分隔"""
        bk_host_id = request.GET.get('bk_host_id')
        client = get_client_by_request(request)
        kwargs = {
            # "bk_host_id": "31,32",
            "bk_host_id": bk_host_id,
        }
        info = client.cc.delete_host(kwargs)
        return JsonResponse(info)

    @classmethod
    def add_host_lock(cls, request):
        """根据主机的 id 对主机加锁，多个以逗号分隔"""
        id_list = request.GET.get('id_list')
        client = get_client_by_request(request)
        kwargs = {
            "id_list": [int(i) for i in id_list.split(',')]
        }
        info = client.cc.add_host_lock(kwargs)
        return JsonResponse(info)

    @classmethod
    def delete_host_lock(cls, request):
        """根据主机 ID 删除主机锁，多个以逗号分隔"""
        id_list = request.GET.get('id_list')
        client = get_client_by_request(request)
        kwargs = {
            "id_list": [int(i) for i in id_list.split(',')]
        }
        info = client.cc.delete_host_lock(kwargs)
        return JsonResponse(info)

    @classmethod
    def clone_host_property(cls, request):
        """克隆主机属性"""
        bk_biz_id = request.GET.get('bk_biz_id')
        bk_org_ip = request.GET.get('bk_org_ip')
        bk_dst_ip = request.GET.get('bk_dst_ip')
        client = get_client_by_request(request)
        kwargs = {
            "bk_biz_id": int(bk_biz_id),  # 主机必须在该业务下
            "bk_org_ip": bk_org_ip,  # 源主机 ip, 只支持传入单 ip
            # "bk_org_ip": "172.27.0.96",  # 源主机 ip, 只支持传入单 ip
            "bk_dst_ip": bk_dst_ip,  # 目标主机 ip, 多个 ip 用","分割
            # "bk_dst_ip": "10.0.0.4",  # 目标主机 ip, 多个 ip 用","分割
            "bk_cloud_id": 0
        }
        info = client.cc.clone_host_property(kwargs)
        return JsonResponse(info)

    # ======================================
    @classmethod
    def list_service_category(cls, request):
        """查询服务分类列表，根据业务 ID 查询，共用服务分类也会返回"""
        bk_biz_id = request.GET.get('bk_biz_id', 2)
        client = get_client_by_request(request)
        kwargs = {
            "bk_biz_id": bk_biz_id
        }

        info = client.cc.list_service_category(kwargs)  # 接口文档有误，不传参数也可访问，且业务id为0
        """
        返回结果
        id	integer	服务分类 ID	
        name	string	服务分类名称	
        bk_root_id	integer	根服务分类 ID	
        bk_parent_id	integer	父服务分类 ID	
        is_built_in	bool	是否内置
        """
        return JsonResponse({"data": info['data']})

    @classmethod
    def create_service_category(cls, request):
        """创建服务分类"""
        bk_biz_id = request.GET.get('bk_biz_id')
        name = request.GET.get('name')
        client = get_client_by_request(request)
        kwargs = {
            # "bk_biz_id": int(bk_biz_id),
            "bk_biz_id": 2,
            # "name": name
            "name": "test102"
        }
        info = client.cc.create_service_category(kwargs)
        return JsonResponse(info)

    @classmethod
    def delete_service_category(cls, request):
        """根据服务分类 ID 删除服务分类"""
        category_id = request.GET.get('category_id')
        client = get_client_by_request(request)
        kwargs = {
            # "id": int(category_id)
            "id": 22
        }
        info = client.cc.delete_service_category(kwargs)
        return JsonResponse(info)

    @classmethod
    def update_service_category(cls, request):
        """更新服务模板信息（目前仅名称字段可更新）"""
        name = request.GET.get('name')
        category_id = request.GET.get('category_id')
        client = get_client_by_request(request)
        kwargs = {
            "id": 21,
            # "id": int(category_id),
            "name": "test1111111"
            # "name": name
        }
        info = client.cc.update_service_category(kwargs)
        return JsonResponse(info)
    # ==================================
