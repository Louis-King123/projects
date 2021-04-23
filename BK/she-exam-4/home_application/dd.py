from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import datetime
# 开启定时工作
scheduler_plan = BackgroundScheduler()  ##实例化调度器
# try:
# 调度器使用DjangoJobStore()
scheduler_plan.add_jobstore(DjangoJobStore(), "default")


# 设置定时任务，选择方式为interval，时间间隔为15 minutes
# 另一种方式为周一到周五固定时间执行任务，对应代码为：
# @register_job(scheduler_plan, 'cron', day_of_week='mon-fri', hour='8', minute='30', second='10',id='task_time')
# @register_job(scheduler_plan, "interval", id="myJob", seconds=30, replace_existing=True)
def my_job():

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# register_events(scheduler_plan)

# @register_job(scheduler_plan, "interval", seconds=5, replace_existing=True)
# def my_job2():
#     print('22222222222')
#
#
# @register_job(scheduler_plan, "interval", seconds=5, replace_existing=True)
# def my_job3():
#     print('33333333333')


# register_events(scheduler_plan)

# scheduler_plan.start()
# except Exception as e:
#     print(e)
#     # 有错误就停止定时器
#     scheduler_plan.shutdown()
