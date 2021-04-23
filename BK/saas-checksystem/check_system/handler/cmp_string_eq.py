# -*- coding: utf-8 -*-


def process(raw_log, quota_name, threshold):
    """
    字符串等于的比较

    @param raw_log: 原始日志
    @param quota_name: 指标名称
    @param threshold: 阈值/对比值

    @return 执行状态, 处理之后的日志, 是否报警
    """
    try:
        result = {}
        for ip_log in raw_log:
            result[ip_log["ip"]] = {}
            # 值
            result[ip_log["ip"]][quota_name] = ip_log["content"].strip('\n')
            result[ip_log["ip"]][quota_name+"_warning"] = result[ip_log["ip"]][quota_name] == threshold
        return True, result
    except ValueError:
        return False, {}
