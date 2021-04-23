import datetime

# import json
from django.http import JsonResponse
# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
#
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), 'default')

from asp_test.utils import TimeTools


# 与前端的接口
def test_add_task(request):
    seconds_time = request.GET.get('seconds')
    # print(seconds_time)
    # kw = {'name': "myJob", 'id': "myJob", 'seconds': int(seconds_time), 'replace_existing': True}
    # scheduler.add_job(my_job, 'interval', name="myJob", id="myJob", seconds=int(seconds_time), replace_existing=True)
    # scheduler.add_job(my_job, 'interval', **kw)

    # scheduler.modify_job()
    kw = {'name': "myJob", 'seconds': int(seconds_time), 'trigger': 'interval'}
    kw2 = {'name': "myJob2", 'seconds': int(seconds_time), 'trigger': 'interval'}
    tt = TimeTools('first_ex')
    tt.add_task(my_job, kw)

    ss = TimeTools('first_exs')
    ss.add_task(my_job2, kw2)

    return JsonResponse({"data": "seconds_time=%s" % (str(seconds_time))})


def my_job():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def my_job2():
    print(datetime.datetime.now().strftime("%Y-%m-%d"))
#
#
# def test_modify_task(request):
#     seconds_time = request.GET.get('seconds')
#     name = request.GET.get('name')
#
#     # 获取job id
#     job_id = all_task(name)
#     print(job_id)
#
#     kwargs = {'seconds': int(seconds_time)}
#
#     # scheduler.modify_job(job_id, seconds=seconds_time)
#     # scheduler.modify_job(job_id, kwargs=kwargs)
#
#     # scheduler.modify_job()   result = scheduler.reschedule_job(job_id='insert_time',trigger='interval',seconds=20)
#
#     # temp_dict = {"seconds": int(seconds_time)}
#     temp_trigger = scheduler._create_trigger(trigger='interval', trigger_args=kwargs)
#     scheduler.modify_job(job_id=job_id, trigger=temp_trigger)
#
#     return JsonResponse({"data": "seconds_time=%s" % (str(seconds_time))})
#
#
# def all_task(name):
#     all = scheduler.get_jobs()
#     for a in all:
#         if a.name == name:
#             return a.id
#     else:
#         return None
#
#
# def get_all_job(request):
#     # all = scheduler.get_jobs()
#     all = scheduler.get_job('myJob')
#     for a in all:
#         print(a)
#     return JsonResponse({"data": "seconds_time=%s"})
#
#
# def init_task(request):
#     seconds_time = 5
#     # print(seconds_time)
#     # scheduler.add_job(my_job, 'interval', name="myJob", id="myJob", seconds=int(seconds_time), replace_existing=True)
#
#     # scheduler.modify_job()
#
#     kw = {'name': "myJob", 'id': "myJob", 'seconds': int(seconds_time), 'replace_existing': True}
#     # scheduler.add_job(my_job, 'interval', name="myJob", id="myJob", seconds=int(seconds_time), replace_existing=True)
#     scheduler.add_job(my_job, trigger='interval', **kw)
#
#     return JsonResponse({"data": "seconds_time=%s" % (str(seconds_time))})
#
#
# def remove_all(request):
#     scheduler.remove_all_jobs()
#     scheduler.remove_job()
#     return JsonResponse({"data": "seconds_time=%s"})
#
#
# # register_events(scheduler)
# scheduler.start()
