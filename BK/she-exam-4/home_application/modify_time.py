import datetime

# from home_application.scp import my_job
#
import json
from django.http import JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


# 与前端的接口
def test_add_task(request):
    seconds_time = request.GET.get('seconds')
    print(seconds_time)
    print(scheduler.add_job(my_job, 'interval', seconds=int(seconds_time), replace_existing=True))

    # scheduler.modify_job()

    return JsonResponse({"data": "seconds_time=%s" % (str(seconds_time))})


def my_job():

    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


register_events(scheduler)
scheduler.start()
