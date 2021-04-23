from check_system.common.utils import get_user_detail, send

# 联系信息
from check_system.models import TaskNotify, Task
from check_system.models.execute_log import ExecuteLog
from check_system.models.models import SystemConfig

content_info = {
    "mail": {
        "title": "巡检结果",
        "content": ""
    },
    "weixin": {
        "heading": "巡检结果",
        "message": ""
    },
    "sms": {
        "content": ""
    }
}


def send_notify(task_id):
    result = {"result": False, "message": "", "send_info": [], "send_type": None}
    error_count = 0
    success_count = 0

    # 查询配置的通知方式
    config = SystemConfig.objects.filter(config_type="消息通知", is_deleted=0).first()
    if not config.config_value:
        result['message'] = "Notify config does not exist"
        return result
    send_type = config.config_value.split(",")

    # 查询任务下的通知用户
    notify_users = TaskNotify.objects.filter(task_id=task_id, is_deleted=0)
    users = ','.join([user['username'] for user in notify_users.values('username')])
    if not notify_users.exists():
        result['message'] = "Notify User does not exist"
        return result

    # 封装通知内容
    task_result = Task.objects.get(pk=task_id)
    execute_result = ExecuteLog.objects.filter(task_id=task_id).first()
    execute_state = [state for code, state in execute_result.STATE_CHOICES if execute_result.exec_state == code][0]

    execute_result = execute_result.to_dict()
    task_content = f"任务：{task_result.task_name}{execute_state}，\n" \
                   f"执行人：{execute_result['operator']}，\n" \
                   f"执行时间：{execute_result['created_time']}，\n" \
                   f"结束时间：{execute_result['end_time']}"
    # 循环通知方式
    for s_type in send_type:

        # 配置相应的内容
        content = content_info[s_type]
        if s_type == "weixin":
            content['receiver'] = users
            content['message'] = task_content
        else:
            content['receiver__username'] = users
            content['content'] = task_content

        send_func = getattr(send, s_type)
        if send_func:
            res = send_func(**content)
            if res.get("result", False):
                success_count += 1
            else:
                error_count += 1
            res['username'] = users
            res['send_type'] = s_type
            result["send_info"].append(res)

    if error_count:
        result.update({
            "result": False,
            "message": "send error",
            "send_type": config.config_value
        })
    else:
        result.update({
            "result": True,
            "message": "success",
            "send_type": config.config_value
        })
    return result
