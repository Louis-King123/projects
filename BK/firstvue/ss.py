dd = {'error_detail2': [
            # 系统检查类型  # 异常个数  # 异常信息
            {'class_name': '安全配置信息', 'error_count': len('safe_config_error'),
             'error_info': 'safe_config_error', 'tag': 'safe_config'},
            {'class_name': '系统运行状态信息', 'error_count': len('system_run_status_error'),
             'error_info': 'system_run_status_error', 'tag': 'system_run_status'},
            {'class_name': '系统性能信息', 'error_count': len('system_performance_error'),
             'error_info': 'system_performance_error', 'tag': 'system_performance'},
            {},
            {}
        ]}

# print(dd)
#
# rows_by_name = sorted(dd['error_detail2'], key=lambda r: r['error_count'] if r else 0,  reverse=True)
#
# print('-----------------------')
# print(rows_by_name)

import copy

data_list = [
  {"ip": "123", "business": "321", "model": 'www'},
  {"ip": "345", "business": "321", "model": 'www'},
  {"ip": "678", "business": "23", "model": 'www'},
  {"ip": "fff", "business": "yu", "model": 'www'},
  {"ip": "ddd", "business": "rt", "model": 'kl'},
  {"ip": "ggg", "business": "hh", "model": 'yh'}
]

for i in data_list:
  business = i['business']
  model = i['model']


dde = {
                "topo": [
                    {
                        "bk_set_id": 10,
                        "module": [
                            {
                                "bk_module_name": "consul",
                                "bk_module_id": 52
                            },
                            {
                                "bk_module_name": "redis",
                                "bk_module_id": 60
                            },
                            {
                                "bk_module_name": "elasticsearch",
                                "bk_module_id": 53
                            }
                        ],
                        "bk_set_name": "公共组件"
                    },
                    {
                        "bk_set_id": 8,
                        "module": [
                            {
                                "bk_module_name": "license",
                                "bk_module_id": 37
                            },
                            {
                                "bk_module_name": "gse_api",
                                "bk_module_id": 29
                            },
                            {
                                "bk_module_name": "gse_task",
                                "bk_module_id": 35
                            },
                            {
                                "bk_module_name": "gse_btsvr",
                                "bk_module_id": 31
                            },
                            {
                                "bk_module_name": "gse_data",
                                "bk_module_id": 32
                            },
                            {
                                "bk_module_name": "gse_dba",
                                "bk_module_id": 33
                            },
                            {
                                "bk_module_name": "gse_alarm",
                                "bk_module_id": 30
                            },
                            {
                                "bk_module_name": "gse_syncdata",
                                "bk_module_id": 36
                            },
                            {
                                "bk_module_name": "gse_proc",
                                "bk_module_id": 34
                            }
                        ],
                        "bk_set_name": "管控平台"
                    },
                    {
                        "bk_set_id": 5,
                        "module": [
                            {
                                "bk_module_name": "bk-iam",
                                "bk_module_id": 15
                            },
                            {
                                "bk_module_name": "bk-ssm",
                                "bk_module_id": 16
                            },
                            {
                                "bk_module_name": "usermgr",
                                "bk_module_id": 17
                            }
                        ],
                        "bk_set_name": "用户认证平台"
                    }
                ],
                "host": {
                    "bk_os_type": "1",
                    "bk_mac": "00:50:56:92:92:24",
                    "bk_host_id": 1,
                    "bk_cloud_id": 0,
                    "bk_host_innerip": "10.0.6.23"
                }
            }
"""
{
                "topo": [
                    {
                        "bk_set_id": 10,
                        "module": [
                            {
                                "bk_module_name": "consul",
                                "bk_module_id": 52
                            },
                            {
                                "bk_module_name": "nginx",
                                "bk_module_id": 58
                            },
                            {
                                "bk_module_name": "consul-template",
                                "bk_module_id": 62
                            },
                            {
                                "bk_module_name": "rabbitmq",
                                "bk_module_id": 59
                            },
                            {
                                "bk_module_name": "mongodb",
                                "bk_module_id": 56
                            },
                            {
                                "bk_module_name": "influxdb",
                                "bk_module_id": 54
                            },
                            {
                                "bk_module_name": "beanstalk",
                                "bk_module_id": 51
                            }
                        ],
                        "bk_set_name": "公共组件"
                    },
                    {
                        "bk_set_id": 4,
                        "module": [
                            {
                                "bk_module_name": "appo",
                                "bk_module_id": 13
                            }
                        ],
                        "bk_set_name": "PaaS平台"
                    },
                    {
                        "bk_set_id": 13,
                        "module": [
                            {
                                "bk_module_name": "fta-api",
                                "bk_module_id": 65
                            }
                        ],
                        "bk_set_name": "故障自愈"
                    }
                ],
                "host": {
                    "bk_os_type": "1",
                    "bk_mac": "00:50:56:92:2b:ae",
                    "bk_host_id": 2,
                    "bk_cloud_id": 0,
                    "bk_host_innerip": "10.0.6.24"
                }
            },
            {
                "topo": [
                    {
                        "bk_set_id": 10,
                        "module": [
                            {
                                "bk_module_name": "consul",
                                "bk_module_id": 52
                            },
                            {
                                "bk_module_name": "mysql",
                                "bk_module_id": 57
                            },
                            {
                                "bk_module_name": "consul-template",
                                "bk_module_id": 62
                            },
                            {
                                "bk_module_name": "zookeeper",
                                "bk_module_id": 61
                            },
                            {
                                "bk_module_name": "kafka",
                                "bk_module_id": 55
                            }
                        ],
                        "bk_set_name": "公共组件"
                    },
                    {
                        "bk_set_id": 4,
                        "module": [
                            {
                                "bk_module_name": "paas",
                                "bk_module_id": 9
                            },
                            {
                                "bk_module_name": "appengine",
                                "bk_module_id": 8
                            },
                            {
                                "bk_module_name": "esb",
                                "bk_module_id": 10
                            },
                            {
                                "bk_module_name": "login",
                                "bk_module_id": 11
                            },
                            {
                                "bk_module_name": "apigw",
                                "bk_module_id": 12
                            },
                            {
                                "bk_module_name": "appt",
                                "bk_module_id": 14
                            }
                        ],
                        "bk_set_name": "PaaS平台"
                    },
                    {
                        "bk_set_id": 9,
                        "module": [
                            {
                                "bk_module_name": "cmdb-admin",
                                "bk_module_id": 38
                            },
                            {
                                "bk_module_name": "cmdb-api",
                                "bk_module_id": 39
                            },
                            {
                                "bk_module_name": "cmdb-auth",
                                "bk_module_id": 40
                            },
                            {
                                "bk_module_name": "cmdb-cloud",
                                "bk_module_id": 41
                            },
                            {
                                "bk_module_name": "cmdb-core",
                                "bk_module_id": 42
                            },
                            {
                                "bk_module_name": "cmdb-datacollection",
                                "bk_module_id": 43
                            },
                            {
                                "bk_module_name": "cmdb-event",
                                "bk_module_id": 44
                            },
                            {
                                "bk_module_name": "cmdb-host",
                                "bk_module_id": 45
                            },
                            {
                                "bk_module_name": "cmdb-op",
                                "bk_module_id": 46
                            },
                            {
                                "bk_module_name": "cmdb-proc",
                                "bk_module_id": 47
                            },
                            {
                                "bk_module_name": "cmdb-task",
                                "bk_module_id": 48
                            },
                            {
                                "bk_module_name": "cmdb-topo",
                                "bk_module_id": 49
                            },
                            {
                                "bk_module_name": "cmdb-web",
                                "bk_module_id": 50
                            }
                        ],
                        "bk_set_name": "配置平台"
                    },
                    {
                        "bk_set_id": 6,
                        "module": [
                            {
                                "bk_module_name": "job-config",
                                "bk_module_id": 18
                            },
                            {
                                "bk_module_name": "job-gateway",
                                "bk_module_id": 21
                            },
                            {
                                "bk_module_name": "job-manage",
                                "bk_module_id": 23
                            },
                            {
                                "bk_module_name": "job-execute",
                                "bk_module_id": 20
                            },
                            {
                                "bk_module_name": "job-crontab",
                                "bk_module_id": 19
                            },
                            {
                                "bk_module_name": "job-logsvr",
                                "bk_module_id": 22
                            },
                            {
                                "bk_module_name": "job-backup",
                                "bk_module_id": 24
                            }
                        ],
                        "bk_set_name": "作业平台v3"
                    },
                    {
                        "bk_set_id": 11,
                        "module": [
                            {
                                "bk_module_name": "nodeman-api",
                                "bk_module_id": 63
                            }
                        ],
                        "bk_set_name": "节点管理"
                    }
                ],
                "host": {
                    "bk_os_type": "1",
                    "bk_mac": "00:50:56:92:a3:23",
                    "bk_host_id": 3,
                    "bk_cloud_id": 0,
                    "bk_host_innerip": "10.0.6.25"
                }
            },
            {
                "topo": [
                    {
                        "bk_set_id": 16,
                        "module": [
                            {
                                "bk_module_name": "ci-gateway",
                                "bk_module_id": 70
                            },
                            {
                                "bk_module_name": "ci-agentless",
                                "bk_module_id": 72
                            },
                            {
                                "bk_module_name": "ci-artifactory",
                                "bk_module_id": 73
                            },
                            {
                                "bk_module_name": "ci-auth",
                                "bk_module_id": 74
                            },
                            {
                                "bk_module_name": "ci-dispatch",
                                "bk_module_id": 75
                            },
                            {
                                "bk_module_name": "ci-environment",
                                "bk_module_id": 76
                            },
                            {
                                "bk_module_name": "ci-image",
                                "bk_module_id": 77
                            },
                            {
                                "bk_module_name": "ci-log",
                                "bk_module_id": 78
                            },
                            {
                                "bk_module_name": "ci-misc",
                                "bk_module_id": 79
                            },
                            {
                                "bk_module_name": "ci-notify",
                                "bk_module_id": 80
                            },
                            {
                                "bk_module_name": "ci-openapi",
                                "bk_module_id": 81
                            },
                            {
                                "bk_module_name": "ci-plugin",
                                "bk_module_id": 82
                            },
                            {
                                "bk_module_name": "ci-process",
                                "bk_module_id": 83
                            },
                            {
                                "bk_module_name": "ci-project",
                                "bk_module_id": 84
                            },
                            {
                                "bk_module_name": "ci-quality",
                                "bk_module_id": 85
                            },
                            {
                                "bk_module_name": "ci-repository",
                                "bk_module_id": 86
                            },
                            {
                                "bk_module_name": "ci-store",
                                "bk_module_id": 87
                            },
                            {
                                "bk_module_name": "ci-ticket",
                                "bk_module_id": 88
                            },
                            {
                                "bk_module_name": "ci-websocket",
                                "bk_module_id": 89
                            }
                        ],
                        "bk_set_name": "蓝盾"
                    }
                ],
                "host": {
                    "bk_os_type": "1",
                    "bk_mac": "00:50:56:92:20:e0",
                    "bk_host_id": 10,
                    "bk_cloud_id": 0,
                    "bk_host_innerip": "10.0.6.33"
                }
            },
            {
                "topo": [
                    {
                        "bk_set_id": 16,
                        "module": [
                            {
                                "bk_module_name": "ci-dockerhost",
                                "bk_module_id": 71
                            }
                        ],
                        "bk_set_name": "蓝盾"
                    }
                ],
                "host": {
                    "bk_os_type": "1",
                    "bk_mac": "00:50:56:92:7f:6f",
                    "bk_host_id": 11,
                    "bk_cloud_id": 0,
                    "bk_host_innerip": "10.0.6.34"
                }
            },
            {
                "topo": [
                    {
                        "bk_set_id": 2,
                        "module": [
                            {
                                "bk_module_name": "空闲机",
                                "bk_module_id": 3
                            }
                        ],
                        "bk_set_name": "空闲机池"
                    }
                ],
                "host": {
                    "bk_os_type": "2",
                    "bk_mac": "",
                    "bk_host_id": 16,
                    "bk_cloud_id": 0,
                    "bk_host_innerip": "10.0.6.29"
                }
            }
"""


# Filename : test.py
# author by : www.runoob.com
d = 0
def recur_fibo(n):
  """递归函数
  输出斐波那契数列"""

  if n <= 1:
    global d
    g = d + n
    print(g)
    return n
  else:
    # print(n)
    return recur_fibo(n - 1) + recur_fibo(n - 2)


# 获取用户输入
# nterms = 10
#
# # 检查输入的数字是否正确
# if nterms <= 0:
#   print("输入正数")
# else:
#   print("斐波那契数列:")
#   for i in range(nterms):
#     print(recur_fibo(i))
#     print(i, '------')
# print(recur_fibo(9))
recur_fibo(9)
print(recur_fibo(9), '-----')

                         6
             5                                       4
             4                        3              3                  2
             3              2         2     1        2    1             1 0
             2     1        1 0       1 0   1        1 0
             1  0  1
             1










