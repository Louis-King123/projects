# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

scheduler = BackgroundScheduler()
if not scheduler.running:
    scheduler.start()


class TimeTool(object):
    """
    参数说明
        trigger 触发器：三种
            data 日期：    触发任务运行的具体时间 2021-04-09 16：28：30

            interval 间隔：触发任务运行的时间间隔（较常用）
                周期参数：week（int）                  间隔几周
                        days（int）                   间隔几天
                        hours（int）                  间隔几小时
                        minutes（int）                间隔几分钟
                        seconds（int）                间隔几秒
                        start_date（datetime or str） 开始时间
                        end_date（datetime or str）   结束时间

            corn 周期：    触发任务运行周期
                周期参数：year（int or str）               年：4位数字
                        mouth（int or str）               月：（范围1-12）
                        day（int or str）                 日：（范围1-31）
                        week（int or str）                周：（范围1-53）
                        day_of_week（int or str）         周内第几天或星期几（范围0-6 或者 mon，tue，wed，thu，fri，stat，sun）
                        hour（int or str）                时：（范围0-23）
                        minute（int or str）              分：（范围0-59）
                        second（int or str）              秒：（范围0-59）
                        start_date（datetime or str）     开始日期时间
                        end_date（datetime or str）       结束日期时间

        name 名称：任务的名称
        job_id 任务的ID ： 建议使用uuid生成
                            import uuid
                            s = uuid.uuid3(uuid.uuid1(), uuid.uuid4().hex).hex
        使用示例：
            tt = TimeTool()
            kwargs1 = {'trigger': 'corn', 'name': 'name1', 'id':'test1', 'minute': '8, 38'}
            kwargs2 = {'trigger': 'interval', 'name': 'name2', 'id':'test2', 'minute': 10}
            tt.func_job_add(func1, kwargs1)
            tt.func_job_add(func2, kwargs2)
    """

    def __init__(self, job_id=None):
        self.id = job_id
        self.replace_existing = True

    def func_job_add(self, func, kwargs):
        """添加定时任务"""
        if self.id:
            kwargs['id'] = self.id
        kwargs['replace_existing'] = self.replace_existing

        try:
            scheduler.add_job(func, **kwargs)
            return True
        except Exception as e:
            print(str(e))
            return False

    def func_job_modify(self, trigger, kwargs):
        """修改job，例如修改执行时间"""
        kwargs['id'] = self.id
        try:
            trigger_instance = scheduler._create_trigger(trigger=trigger, **kwargs)
            scheduler.modify_job(job_id=self.id, trigger=trigger_instance)
            return True
        except Exception as e:
            print(str(e))
            return False

    def func_job_remove(self):
        """删除指定job_id定时任务"""
        scheduler.remove_job(self.id)

    def func_job_remove_all(self):
        """删除所有定时任务"""
        scheduler.remove_all_jobs()

    def func_job_pause(self):
        """暂停指定job_id定时任务"""
        scheduler.pause_job(self.id)

    def func_job_resume(self):
        """开启指定job_id定时任务"""
        scheduler.resume_job(self.id)



