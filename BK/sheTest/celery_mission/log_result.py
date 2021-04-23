# -*- coding: utf-8 -*-

import time
from celery import task
from blueking.component.shortcuts import get_client_by_user
from home_application.models import History, Logs


@task()
def get_logs(username, biz_id, instance_id, custom_id):
    """
    循环获取12次，总耗时60秒，超时默认失败
    """
    date = {"bk_biz_id": biz_id, "job_instance_id": instance_id}
    client = get_client_by_user(username)
    result = None
    step_id_list = []  # 记录步骤ID
    for i in range(0, 13):
        result = client.job.get_job_instance_status(date)
        if result['data']['job_instance']['status'] == 3:
            # 记录step_instance_list
            step_instance_list = result['data']['step_instance_list']

            for step in step_instance_list:
                step_id_list.append(step['step_instance_id'])

            # 执行成功
            History.objects.filter(log_id=custom_id).update(inst_status=3, inst_finish=True)
            break
        time.sleep(5)
    else:
        # 执行失败
        print('执行失败')
        History.objects.filter(log_id=custom_id).update(inst_status=2, inst_finish=result['data']['finished'])
        return

    # 记录执行结果
    logs_info = Logs.objects.filter(custom_id=custom_id)

    for step_id in step_id_list:
        for log in logs_info:
            ip_log_data = {
                'bk_biz_id': biz_id,
                'job_instance_id': instance_id,
                'step_instance_id': step_id,
                'bk_cloud_id': 0,
                'ip': log.ip,
            }

            log_result = client.job.get_job_instance_ip_log(ip_log_data)
            # print(log.content)
            if len(log.content):
                log.content = log.content + '&&' + log_result['data']['log_content'].strip()
            else:
                log.content = log_result['data']['log_content'].strip()
            log.save()
            # print(log_result)

    return
