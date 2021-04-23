from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore

from app.jobs.report.alert import alert_work
from app.jobs.report.resource_metrice import resouce_metric_work
from app.jobs.report.resource_set import resouce_set_work


class SheduleJob:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_jobstore(DjangoJobStore(), 'default')

    # 注册
    def add_job(self):
        # 每周日 1点 执行上传资源配置数据 到时请取消注释
        # self.scheduler.add_job(resouce_set_work, CronTrigger.from_crontab('0 1 * * 0'), id='resouce_set_work',
        #                        replace_existing=True,
        #                        max_instances=2, misfire_grace_time=180)

        # 这是测试, 到时 请删掉
        self.scheduler.add_job(resouce_set_work, 'cron', minute='*', id='resouce_set_work',
                               replace_existing=True,
                               max_instances=2, misfire_grace_time=180)

        # 资源指标每30分钟上报 到时请取消注释
        # self.scheduler.add_job(resouce_metric_work, 'cron', minute='*/30', id='resouce_metric_work',
        #                        replace_existing=True,
        #                        max_instances=2, misfire_grace_time=180)

        # 这是测试, 到时 请删掉
        self.scheduler.add_job(resouce_metric_work, 'interval', seconds=120, id='resouce_metric_work',
                               replace_existing=True,
                               max_instances=2, misfire_grace_time=180)

        # 故障告警每13分钟上报 到时请取消注释
        # self.scheduler.add_job(alert_work, 'cron', minute='*/13', id='alert_work',
        #                        replace_existing=True,
        #                        max_instances=2, misfire_grace_time=180)

        self.scheduler.add_job(alert_work, 'cron', minute='*/3', id='alert_work',
                               replace_existing=True,
                               max_instances=2, misfire_grace_time=180)

    # 启动
    def start(self):
        self.add_job()
        self.scheduler.start()

    # 停止
    def stop(self):
        pass
        # self.scheduler.shutdown()

    # 暂停
    def pause(self):
        pass
        # self.scheduler.pause_job('job_id')
        # scheduler.pause()

    # 播放
    def resume(self):
        pass
        # self.scheduler.resume_job('job_id')


job = SheduleJob()