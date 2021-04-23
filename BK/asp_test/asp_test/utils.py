from django.http import JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore


scheduler = BackgroundScheduler()
if not scheduler.running:
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.start()


class TimeTools(object):

    def __init__(self, job_id):
        # self.scheduler = BackgroundScheduler()
        # self.scheduler.add_jobstore(DjangoJobStore(), 'default')
        # if not self.scheduler.running:
        #     self.scheduler.start()
        self.id = job_id
        self.replace_existing = True

    # 与前端的接口
    def add_task(self, func, kw):
        kw['id'] = self.id
        kw['replace_existing'] = self.replace_existing
        # kw['name'] = self.name

        scheduler.add_job(func,  **kw)

        return JsonResponse({"data": "seconds_time=%s"})
