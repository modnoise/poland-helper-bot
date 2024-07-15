from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from application.core.scheduler import SchedulerData
from application.jobs.clear_chat import clear_chat


def schedule_jobs(data: SchedulerData, scheduler: AsyncIOScheduler):
    scheduler.add_job(clear_chat, 'interval',
                      minutes=1,
                      start_date=datetime.utcnow(),
                      args=(data,))