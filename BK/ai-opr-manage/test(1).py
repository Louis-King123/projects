# -*- coding: utf-8 -*-
from pprint import pprint
from urllib.parse import urlparse, urlencode
from urllib import request
import urllib
import json
import time
import datetime


class Prometheus(object):
    def __init__(self, ip, port):
        self.base_url = "http://{ip}:{port}/{api_path}?{query_params}"
        self.ip = ip
        self.port = port

    def query(self, query, start, end, step, timeout=None):
        req_data = {
            "query": query,
            "start": start,
            "end": end,
            "step": step
        }
        url = self.base_url.format(
            ip=self.ip,
            port=self.port,
            api_path="/api/v1/query",
            query_params=urlencode(req_data)
        )
        req = request.Request(url=url, method="POST")
        return_status = False
        return_message = ""
        return_data = {}
        try:
            rep = request.urlopen(req).read()
            rep_data = json.loads(rep)
            status = rep_data.get("status")
            if status != "success":
                return_status = False
                return_message = "数据获取失败"
            else:
                result = rep_data.get("result")
                item = result[0]
                ip, _ = item.get("metric", {}).get("instance").split(":")
                _, quota_value = item.get("value")
                return_status = True
                return_data = {
                    "ip": ip,
                    "value": quota_value
                }
        except Exception as e:
            return_status = False
            return_message = repr(e)
        finally:
            return {"status": return_status, "message": return_message, "data": return_data}


def get_monitor_data(prometheus_ip, prometheus_port, query_list):
    prometheus = Prometheus(ip=prometheus_ip, port=prometheus_port)
    current_time = datetime.datetime.now()
    start = str(round(time.mktime((current_time - datetime.timedelta(minutes=2)).timetuple())))
    end = str(round(time.mktime(current_time.timetuple())))
    step = "15"
    result_map = {}
    for i in query_list:
        name = i.get("name")
        query = i.get("query")
        res = prometheus.query(query, start, end, step)
        if not res.get("status"):
            pass
        else:
            ip = res.get("data", {}).get("ip")
            value = res.get("data", {}).get("value")
            if ip not in result_map:
                result_map[ip] = {
                    name: value
                }
            else:
                result_map[ip][name] = value
    return result_map


if __name__ == "__main__":
    """
        81.68.64.205
        121.36.229.103
        124.70.141.107
    """
    prometheus_ip = "121.36.229.103"
    prometheus_port = "9090"
    # CPU使用率
    avg_cpu_query = "100 * (1 - avg(irate(node_cpu_seconds_total{mode='idle'}[10m])) by(instance))"
    # avg_cpu_query = "100 - sum(node_cpu_seconds_total{mode='idle'} * 100)"
    # 内存使用率
    mem_used_rate_query = "(node_memory_MemTotal_bytes-(node_memory_MemFree_bytes+ node_memory_Cached_bytes + node_memory_Buffers_bytes))/node_memory_MemTotal_bytes * 100"
    # mem_used_rate_query = '(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100'
    # 磁盘使用率
    # disk_used_rate = "sum(node_filesystem_free_bytes) by(instance)"
    # disk_used_rate = "sum(node_filesystem_size_bytes) by(instance)"
    # disk_used_rate = "sum(node_filesystem_size_bytes) by(instance)"
    # disk_used_rate = 'sum(node_filesystem_free_bytes{fstype=~"ext4|xfs"})/sum(node_filesystem_size_bytes{fstype=~"ext4|xfs"}) by(instance)'
    # disk_used_rate = "node_filesystem_size_bytes"
    # disk_used_rate = '100 * (node_filesystem_size_bytes{fstype=~"xfs|ext4"} - node_filesystem_avail_bytes) / node_filesystem_size_bytes'
    prometheus = Prometheus(ip=prometheus_ip, port=prometheus_port)
    current_time = datetime.datetime.now()
    start = str(round(time.mktime((current_time - datetime.timedelta(minutes=2)).timetuple())))
    end = str(round(time.mktime(current_time.timetuple())))
    step = "15"

    linux_list = [
        {
            "name": "linux_cpu_rate",
            "query": "100 * (1 - avg(irate(node_cpu_seconds_total{mode='idle'}[10m])) by(instance))"
        },
        {
            "name": "linux_mem_rate",
            "query": "100 * (1 - (node_memory_MemTotal_bytes - (node_memory_MemFree_bytes + node_memory_Cached_bytes + node_memory_Buffers_bytes)) / node_memory_MemTotal_bytes)"
        },
        {
            "name": "linux_disk_free_sum",
            "query": "sum(node_filesystem_free_bytes) by(instance)"
        },
        {
            "name": "linux_disk_size_sum",
            "query": "sum(node_filesystem_size_bytes) by(instance)"
        }
    ]

    windows_list = [
        {
            "name": "windows_cpu_rate",
            "query": "100 * (1 - avg(irate(windows_cpu_time_total{mode='idle'}[2m])) by (instance))"
        },
        {
            "name": "linux_mem_rate",
            "query": "100 * (1- windows_os_physical_memory_free_bytes / windows_cs_physical_memory_bytes)"
        },
        {
            "name": "linux_disk_free_sum",
            "query": "sum(windows_logical_disk_free_bytes) by (instance)"
        },
        {
            "name": "linux_disk_size_sum",
            "query": "sum(windows_logical_disk_size_bytes) by (instance)"
        }
    ]
    linux_cpu_rate = "100 * (1 - avg(irate(node_cpu_seconds_total{mode='idle'}[10m])) by(instance))"
    linux_mem_rate = "100 * (1 - (node_memory_MemTotal_bytes - (node_memory_MemFree_bytes + node_memory_Cached_bytes + node_memory_Buffers_bytes)) / node_memory_MemTotal_bytes)"
    linux_disk_free_sum = "sum(node_filesystem_free_bytes) by(instance)"
    linux_disk_size_sum = "sum(node_filesystem_size_bytes) by(instance)"

    windows_cpu_rate = "100 * (1 - avg(irate(windows_cpu_time_total{mode='idle'}[2m])) by (instance))"
    windows_mem_rate = "100 * (1- windows_os_physical_memory_free_bytes / windows_cs_physical_memory_bytes)"
    windows_disk_free_sum = "sum(windows_logical_disk_free_bytes) by (instance)"
    windows_disk_size_sum = "sum(windows_logical_disk_size_bytes) by (instance)"

    cpu_res = prometheus.query(windows_cpu_rate, start, end, step)
    for i in linux_list:
        name = i.get("name")
        query = i.get("query")
        res = prometheus.query(query, start, end, step)
        print("#" * 30 + name)
        pprint(res)
    print("*" * 100)
    for i in linux_list:
        name = i.get("name")
        query = i.get("query")
        res = prometheus.query(query, start, end, step)
        print("#" * 30 + name)
        pprint(res)
