import base64
import json
import time
import importlib
import datetime
# celery
import uuid

from celery import task
# django
# bk

from blueapps.utils.logger import logger
from blueking.component.shortcuts import get_client_by_user
# check_system
from check_system.common.notify import send_notify
from check_system.decorator import Log
from check_system.models import Quota, CheckSystemOs, CheckSystemClass
from check_system.models.task import Task
from check_system.models.task_result import TaskResult
from check_system.logic.TplLogic import TplLogic
from check_system.link_tool.redis_client import *
from check_system.models.execute_log import ExecuteLog
from check_system.link_tool.tool import Write_Json_File
from check_system.models.task_result import TaskHostResult


@task()
def ceshi_celery(task_obj, task_id, user):
    ExcuteFlow(task_obj, task_id, user).detection()
    return


class ExcuteFlow():

    # 参数初始化
    def __init__(self, task_obj, task_id, user):
        self.task_obj = task_obj
        self.ip_error_list = []
        self.task_id = task_id
        self.user = user
        self.task_tpl_id = task_obj.task_tpl_id
        # self.tpl_quota_list = TplLogic().getQuotas(task_obj.task_tpl_id)

    def refrefsh_quota_list(self):

        tpl_quota_list = TplLogic().getQuotas(self.task_tpl_id)
        return tpl_quota_list

    def refrefsh_list(self, list):
        list = []
        return list

    # 执行流程判断
    def detection(self):
        if self.task_obj.exec_schedule == "instant":
            self.execution(self.task_obj, self.task_id, self.user)
        else:
            exe = ExecuteLog.objects.create(
                work_code=str(uuid.uuid1()),
                exec_state=1,
                task_id=self.task_id,
                operator=self.user
            )
            if self.task_obj.exec_schedule == "interval":
                self.timing_execute(self.task_obj, self.task_id, self.user, exe)
            elif self.task_obj.exec_schedule == "crontab":
                self.period_execute(self.task_obj, self.task_id, self.user, exe)

    # 立即执行
    def execution(self, task, task_id, user):

        self.ip_error_list.clear()
        exe = ExecuteLog.objects.create(
            work_code=str(uuid.uuid1()),
            exec_state=1,
            task_id=self.task_id,
            operator=self.user
        )
        for index, quota in enumerate(self.refrefsh_quota_list()):
            # 1
            task_result_obj = TaskResult.objects.create(
                task=task,
                task_state=0,
                task_step_state=0,
                quota_id=int(quota['id']),
            )
            task_result = TaskResult.objects.filter(id=task_result_obj.id)
            # 执行前修改表状态
            # 任务结果表
            task_result.update(task_state=1)
            self.execute_script(task_result_obj, task_result, quota, exe.id)
            # 判断是否是脚本列表的最后一组数据
            if index >= len(self.refrefsh_quota_list()) - 1:
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 任务结果表
                task_result.update(task_state=2)
                # 任务表
                Task.objects.filter(id=task.id).update(exec_state=0)
                # 删除redis缓存状态
                redis_link.hdel('current_task', self.task_id)
                # 历史记录表
                ExecuteLog.objects.filter(id=exe.id).update(exec_state=2, end_time=dt)
                redis_link.delete("current_task")

                # 通知
                notify_result = send_notify(task_id)
                logger.info(f"发送通知 总状态({notify_result['result']}) 发送方式({notify_result['send_type']}) 发送详情({notify_result['send_info']})")
                return

    # 定时执行
    def timing_execute(self, task, task_id, user, exe):

        for index, quota in enumerate(self.refrefsh_quota_list()):
            # 1
            task_result_obj = TaskResult.objects.create(
                task=task,
                task_state=0,
                task_step_state=0,
                quota_id=int(quota['id']),
            )
            task_result = TaskResult.objects.filter(id=task_result_obj.id)
            task_result.update(task_state=1)

            date_time = datetime.datetime.strptime(self.task_obj.exec_start_time, '%Y-%m-%d %H:%M:%S')
            time_time = str(time.mktime(date_time.timetuple()))  # 1609344000.0
            # 控制周期任务时间间隔
            if redis_link.get(name=task_id):
                # 如果任务已经完成，就删除当前任务继续添加新的任务
                redis_task = eval(str(redis_link.get(name=task_id), 'utf-8'))
                if redis_task['status'] == 'executed':
                    redis_link.delete(task_id)
                    redis_link.set(name=task_id,
                                   value=f"{{'time_second':{time_time}, 'plan':'interval', 'status': 'unexecuted'}}"
                                   )
            else:
                # 创建新的任务放入队列
                redis_link.set(name=task_id,
                               value=f"{{'time_second':{time_time}, 'plan':'interval', 'status': 'unexecuted'}}")
                redis_task = eval(str(redis_link.get(name=task_id), 'utf-8'))

            while True:
                if (time.time() - int(redis_task['time_second'])) >= 0:
                    # 执行前修改表状态
                    # 任务结果表
                    task_result.update(task_state=0)
                    # 定时执行

                    # 每执行成功一次就把列表中的脚本删除，添加进新的列表当中

                    self.execute_script(task_result_obj, task_result, quota, exe.id)

                    # # 判断如果当前脚本是脚本列的最后一个，执行结束就改变redis状态,并删除
                    if index >= len(self.refrefsh_quota_list()) - 1:
                        redis_link.set(name=task_id,
                                       value=f"{{'time_second':{time_time}, 'plan':'interval', 'status': 'executed'}}")
                        redis_link.delete(task_id)

                        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # 任务结果表
                        task_result.update(task_state=2)
                        # 任务表
                        Task.objects.filter(id=task.id).update(exec_state=0)
                        # 历史记录表
                        ExecuteLog.objects.filter(id=exe.id).update(exec_state=2, end_time=dt)
                        # 删除本次的执行状态
                        redis_link.hdel('current_task', task_id)
                        return
                    break
                time.sleep(2)
        pass

    # 周期执行
    def period_execute(self, task, task_id, user, exe):

        task_result_obj = TaskResult.objects.create(
            task=task,
            task_state=1,
            task_step_state=0,
            quota_id=0,
        )
        task_result = TaskResult.objects.filter(id=task_result_obj.id)

        # 当前时间 + 周期天数 = 执行日期
        time_time = str(time.time() + (int(task.exec_timece) * 86400))  # now_time + 1 * 86400
        # time_time = str(time.time()+10)
        if redis_link.get(name=task_id):
            # 如果任务已经完成，就删除当前任务继续添加新的任务
            redis_task = eval(str(redis_link.get(name=task_id), 'utf-8'))
            if redis_task['status'] == 'executed':
                redis_link.delete(task_id)
                redis_link.set(name=task_id,
                               value=f"{{'time_second':{time_time}, 'plan':'crontab', 'status': 'unexecuted'}}"
                               )
        else:
            # 创建新的任务放入队列
            redis_link.set(name=task_id,
                           value=f"{{'time_second':{time_time}, 'plan':'crontab', 'status': 'unexecuted'}}")
            redis_task = eval(str(redis_link.get(name=task_id), 'utf-8'))
        task_status = True
        time_start = int(redis_task['time_second'])
        while task_status:
            if (time.time() - time_start) >= 0:
                redis_link.hset(name="current_task", key=task_id, value="True")
                for index, quota in enumerate(self.refrefsh_quota_list()):
                    # 周期执行
                    # 判断当前任务执行状态成为完成的话，就终止整个celery
                    # redis将本次任务执行存入，防止并发执行
                    self.execute_script(task_result_obj, task_result, quota, exe.id)

                    # 判断状态如果是完成就终止
                    if redis_task['status'] == "executed":
                        redis_link.delete(task_id)
                        # 任务表
                        Task.objects.filter(id=task.id).update(exec_state=0)
                        # 停止循环
                        task_status = False
                        return

                    if index == len(self.tpl_quota_list) - 1:
                        # 判断当前脚本是脚本列的最后一位就重置任务时间

                        # 下一次执行的时间
                        time_time = time.time() + (int(task.exec_timece) * 86400)
                        # redis_link.set(name=task_id,
                        #                value=f"{{'time_second':{time_time}, 'plan':'crontab', 'status': 'unexecuted'}}")
                        time_start = time_time
                        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # 任务结果表
                        task_result.update(task_state=2)
                        # 历史记录表
                        ExecuteLog.objects.filter(id=exe.id).update(exec_state=2, end_time=dt)
                        # 删除本次的执行状态
                        redis_link.hdel('current_task', task_id)
                        # 初始化IP_error_list
                        self.ip_error_list = self.refrefsh_list
                        # 创建好新的记录
                        ExecuteLog.objects.create(
                            work_code=str(uuid.uuid1()),
                            exec_state=1,
                            task_id=self.task_id,
                            operator=self.user
                        )
                    time.sleep(1)
            time.sleep(2)

    # 执行任务
    def execute_script(self, task_result_obj, task_result, quota, execute_id):
        tpl_task_obj = task_result_obj.task
        BK_BIZ_ID = tpl_task_obj.exec_biz_id
        tpl_quota_obj = quota
        Task.objects.filter(id=tpl_task_obj.id).update(exec_state=1)
        exec_hosts = tpl_task_obj.exec_hosts
        ip_lists = [{"bk_cloud_id": 0, "ip": h['bk_host_innerip']} for h in eval(exec_hosts)]

        exec_acc = tpl_task_obj.exec_acc
        script_type = tpl_quota_obj['script_type']
        script_content = tpl_quota_obj['script_content']
        # 脚本内容base64
        script_content = str(base64.b64encode(script_content.encode("utf8")), "utf8")
        # 任务名称
        task_name = tpl_task_obj.task_name + "_" + tpl_quota_obj['quota_name']

        # 初始化接口对象
        blue_apis = BlueKAPIS(tpl_task_obj.task_op, BK_BIZ_ID)

        host_error_flag = True
        while host_error_flag:
            for index, data in enumerate(ip_lists):
                if data['ip'] in self.ip_error_list:
                    ip_lists.pop(index)
                    break
            else:
                host_error_flag = False

        res = blue_apis.fast_execute_script(task_name, script_type,
                                            script_content, exec_acc, ip_lists)

        if not res["result"]:
            # 调用详细接口循环执行每个IP
            self.resolve_execute(
                blue_apis,
                tpl_quota_obj,
                task_name,
                script_type,
                script_content,
                exec_acc,
                ip_lists,
                execute_id,
                task_result,
                tpl_task_obj
            )
            return
        job_instance_id = res["data"]["job_instance_id"]

        # 开始循环查询脚本执行状态
        query_count = 0
        while True:

            # 查询超过了限制次数
            if query_count == 25:
                # 调用详细接口循环执行每个IP
                self.resolve_execute(
                    blue_apis,
                    tpl_quota_obj,
                    task_name,
                    script_type,
                    script_content,
                    exec_acc,
                    ip_lists,
                    execute_id,
                    task_result,
                    tpl_task_obj
                )
                return

            query_count += 1

            # 获取执行状态

            res = blue_apis.get_job_instance_status(job_instance_id)

            # 调用[根据作业实例 ID 查询作业执行状态]接口失败
            if not res["result"]:
                task_result.update(task_state=4)
                Task.objects.filter(id=tpl_task_obj.id).update(exec_state=3)
                # 调用详细接口循环执行每个IP
                self.resolve_execute(
                    blue_apis,
                    tpl_quota_obj,
                    task_name,
                    script_type,
                    script_content,
                    exec_acc,
                    ip_lists,
                    execute_id,
                    task_result,
                    tpl_task_obj
                )
                return

            status = res["data"]["job_instance"]["status"]
            task_result.update(task_step_state=status)

            # 作业状态码:
            # 1.未执行; 2.正在执行; 3.执行成功;
            # 4.执行失败; 5.跳过; 6.忽略错误;
            # 7.等待用户; 8.手动结束; 9.状态异常;
            # 10.步骤强制终止中; 11.步骤强制终止成功; 12.步骤强制终止失败

            if status >= 4:  # 脚本执行错误
                task_result.update(task_state=4)
                Task.objects.filter(id=tpl_task_obj.id).update(exec_state=3)
                # 调用详细接口循环执行每个IP
                self.resolve_execute(
                    blue_apis,
                    tpl_quota_obj,
                    task_name,
                    script_type,
                    script_content,
                    exec_acc,
                    ip_lists,
                    execute_id,
                    task_result,
                    tpl_task_obj
                )
                return

            # 判断状态执行完毕
            if res["data"]["is_finished"]:
                task_result.update(task_state=2)

                # 开始查询日志
                res = blue_apis.get_job_instance_log(job_instance_id)
                # 调用[根据作业实例 ID 查询作业执行日志]接口失败
                if not res["result"]:
                    task_result.update(task_state=4)
                    Task.objects.filter(id=tpl_task_obj.id).update(exec_state=3)
                    # 调用详细接口循环执行每个IP
                    self.resolve_execute(
                        blue_apis,
                        tpl_quota_obj,
                        task_name,
                        script_type,
                        script_content,
                        exec_acc,
                        ip_lists,
                        execute_id,
                        task_result,
                        tpl_task_obj
                    )
                    return
                # 获取日志
                ip_logs = res["data"][0]["step_results"][0]["ip_logs"]

                # 源生日志保存
                task_result.update(raw_log=json.dumps(ip_logs))

                # 日志分析函数
                self.resolve_log(ip_logs, tpl_quota_obj, task_result, tpl_task_obj, execute_id)
                return
            time.sleep(2)

    # 失败任务分解执行
    def resolve_execute(self, blue_apis, tpl_quota_obj, task_name, script_type,
                        script_content, exec_acc, ip_lists, execute_id,
                        task_result, tpl_task_obj):
        login = []

        quota_obj = Quota.objects.get(id=tpl_quota_obj['id'])
        system_class = CheckSystemClass.objects.get(id=quota_obj.quota_class)

        for ip_info in ip_lists:
            res = blue_apis.fast_execute_script(
                task_name, script_type,
                script_content, exec_acc, [ip_info]
            )
            fields = {
                "host_ip": ip_info['ip'],
                "quota_id": quota_obj,
                "system_class": system_class,
                "task_id": task_result.first().task,
                "check_result": "powerOff/",
                "recommend_value": tpl_quota_obj['quota_threshold'],
                "result_status": False,
                "execute_log_id": execute_id,
                'os_id': quota_obj.quota_os,
            }

            # 调用[快速执行脚本]接口失败
            if not res["result"]:
                TaskHostResult.objects.create(**fields)
                self.ip_error_list.append(ip_info['ip'])
                continue
            job_instance_id = res["data"]["job_instance_id"]
            # 开始循环查询脚本执行状态
            query_count = 0
            while True:
                # 获取执行状态
                res = blue_apis.get_job_instance_status(job_instance_id)

                # 调用[根据作业实例 ID 查询作业执行状态]接口失败
                if not res["result"]:
                    TaskHostResult.objects.create(**fields)
                    self.ip_error_list.append(ip_info['ip'])
                    break

                status = res["data"]["job_instance"]["status"]

                # 作业状态码:
                # 1.未执行; 2.正在执行; 3.执行成功;
                # 4.执行失败; 5.跳过; 6.忽略错误;
                # 7.等待用户; 8.手动结束; 9.状态异常;
                # 10.步骤强制终止中; 11.步骤强制终止成功; 12.步骤强制终止失败

                if status >= 4:  # 脚本执行错误

                    fields['check_result'] = fields['check_result'] + '巡检失败，错误码：' + str(
                        res['data']['job_instance']['job_instance_id'])
                    TaskHostResult.objects.create(**fields)
                    self.ip_error_list.append(ip_info['ip'])

                    break

                # 判断状态执行完毕
                if res["data"]["is_finished"]:
                    # 开始查询日志
                    res = blue_apis.get_job_instance_log(job_instance_id)
                    # 调用[根据作业实例 ID 查询作业执行日志]接口失败
                    if not res["result"]:
                        TaskHostResult.objects.create(**fields)
                        self.ip_error_list.append(ip_info['ip'])
                        break
                    # 获取日志
                    ip_logs = res["data"][0]["step_results"][0]["ip_logs"]
                    login = ip_logs
                    break
                # 查询超过了限制次数
                if query_count == 10:
                    # 调用详细接口循环执行每个IP

                    TaskHostResult.objects.create(**fields)
                    self.ip_error_list.append(ip_info['ip'])
                query_count += 1
                time.sleep(2)
        if len(login) <= 0:
            return
        else:
            self.resolve_log(login, tpl_quota_obj, task_result, tpl_task_obj, execute_id)
            return login

    # 日志清洗
    def resolve_log(self, ip_logs, tpl_quota_obj, task_result, tpl_task_obj, execute_id):
        # 获取 IP 对应的 日志
        raw_log = [{"ip": log["ip"], "content": log["log_content"]} for log in ip_logs]

        # 解析日志
        quota_handler = tpl_quota_obj['quota_handler'] if tpl_quota_obj['quota_handler'] else 'cmp_show'
        quota_threshold = tpl_quota_obj['quota_threshold']
        quota_name = tpl_quota_obj['quota_name']

        try:
            module = importlib.import_module("check_system.handler." + quota_handler)
            (success, log) = module.process(raw_log, quota_name, quota_threshold)
            if success:
                # 分析成功更改表状态
                task_result.update(task_state=3)

                # True
                # {
                #   '10.0.6.53': {'普通账号UMASK值设置 ': '22\n', '普通账号UMASK值设置 _warning': False}，
                #   '10.0.6.54': {'普通账号UMASK值设置 ': '22\n', '普通账号UMASK值设置 _warning': False}
                # }

                quota_obj = Quota.objects.get(id=tpl_quota_obj['id'])
                system_class = CheckSystemClass.objects.get(id=quota_obj.quota_class)  # 指标类

                quota_threshold_str = self.set_quota_handler(quota_handler)

                for key, value in log.items():
                    result = list(value.values())  # [1, 2]

                    TaskHostResult.objects.create(
                        host_ip=key,
                        quota_id=quota_obj,
                        system_class=system_class,
                        task_id=task_result.first().task,
                        check_result=result[0],
                        recommend_value=quota_threshold_str + tpl_quota_obj['quota_threshold'],
                        result_status=result[1] if isinstance(result[1], bool) else True,
                        execute_log_id=execute_id,
                        os_id=quota_obj.quota_os
                    )
                return
            else:
                # 数据解析出现问题

                task_result.update(task_state=5)
        except Exception as e:
            task_result.update(task_state=5)
            return

        # 更新任务的进度
        progress = TaskResult.objects.filter(task=tpl_task_obj, task_state=3).count()
        Task.objects.filter(id=tpl_task_obj.id, exec_progress__lt=progress).update(exec_progress=progress)
        Task.objects.filter(id=tpl_task_obj.id, exec_quota_total=progress).update(exec_state=2,
                                                                                  end_time=datetime.datetime.now())

        return

    def set_quota_handler(self, handler):

        handlerList = handler.split('_')
        if 'eq' in handlerList:
            return ''
        elif 'neq' in handlerList:
            return '!='
        elif 'gt' in handlerList:
            return '>'
        elif 'gte' in handlerList:
            return '>='
        elif 'lt' in handlerList:
            return '<'
        elif 'lte' in handlerList:
            return '<='
        # elif 'disk' in handlerList:
        #     return '磁盘内容:'
        # elif 'show' in handlerList:
        #     return '展示:'
        else:
            return ''


# 蓝鲸接口
class BlueKAPIS():

    def __init__(self, user, BK_BIZ_ID):
        self.user = user
        self.bk_biz_id = BK_BIZ_ID

    def fast_execute_script(self, task_name, script_type,
                            script_content, exec_acc, ip_lists
                            ):
        client = get_client_by_user(self.user)
        res = client.job.fast_execute_script({
            "bk_biz_id": self.bk_biz_id,
            "script_timeout": 100,
            "task_name": task_name,
            "script_type": script_type,
            "script_content": script_content,
            "account": exec_acc,
            "ip_list": ip_lists
        })
        return res

    def get_job_instance_status(self, job_instance_id):
        # 获取执行状态
        client = get_client_by_user(self.user)
        res = client.job.get_job_instance_status({
            "bk_biz_id": self.bk_biz_id,
            "job_instance_id": job_instance_id
        })

        return res

    def get_job_instance_log(self, job_instance_id):
        # 开始查询日志
        client = get_client_by_user(self.user)
        res = client.job.get_job_instance_log({
            "bk_biz_id": self.bk_biz_id,
            "job_instance_id": job_instance_id
        })
        return res
