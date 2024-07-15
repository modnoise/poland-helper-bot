from dataclasses import dataclass

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker


@dataclass
class SchedulerData:
    scheduler: AsyncIOScheduler
    session_pool: async_sessionmaker
    bot: Bot
