{"code": 0, "permission": None, "result": True, "request_id": "b51de6014edf4df297222f2e1cdbcbc9", "message": "success", "data": [{"host_count": 0, "default": 0, "bk_obj_name": "业务", "bk_obj_id": "biz", "child": [{"host_count": 0, "default": 0, "bk_obj_name": 群", "bk_obj_id": "set", "child": [{"host_count": 0, "default": 0, "bk_obj_name": "模块", "bk_obj_id": "module", "child": [], "bk_inst_id": 101, "bk_inst_name": "测试模块"}, {"host_count": 0, "default": 0, "bk_obj_name": "模块", "bk_obj_id": "module", "child": nst_id": 103, "bk_inst_name": "测试模块1"}], "bk_inst_id": 30, "bk_inst_name": "测试01"}, {"host_count": 0, "default": 0, "bk_obj_name": "集群", "bk_obj_id": "set", "child": [{"host_count": 0, "default": 0, "bk_obj_name": "模块", "bk_obj_id": "module", "child":nst_id": 102, "bk_inst_name": "权限模块测试"}], "bk_inst_id": 31, "bk_inst_name": "权限测试"}, {"host_count": 0, "default": 0, "bk_obj_name": "集群", "bk_obj_id": "set", "child": [], "bk_inst_id": 29, "bk_inst_name": "同步测试"}], "bk_inst_id": 6, "bk_inst_name自动发布"}]}


from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

#开启定时工作
scheduler_plan = BackgroundScheduler()  ##实例化调度器
try:
    # 调度器使用DjangoJobStore()
    scheduler_plan.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为15 minutes
    # 另一种方式为周一到周五固定时间执行任务，对应代码为：
    # @register_job(scheduler_plan, 'cron', day_of_week='mon-fri', hour='8', minute='30', second='10',id='task_time')
    @register_job(scheduler_plan,"interval", minutes=15)
    def my_job():
        # 这里写你要执行的任务
        pass
    register_events(scheduler_plan)
    scheduler_plan.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler_plan.shutdown()
