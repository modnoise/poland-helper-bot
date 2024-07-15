import asyncio
import logging

import betterlogging as bl
import openai
import pytz
import alembic
from aiogram import Bot, Dispatcher
from aiogram.enums import ContentType
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.i18n import I18n
from alembic import command
from alembic.config import Config as alembic_config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.core.scheduler import SchedulerData
from application.jobs import schedule_jobs
from infrastructure.database.seed import seed_data
from infrastructure.database.setup import create_session_pool, create_engine
from tgbot.config import load_config, Config
from tgbot.dialogs import setup_all_dialogs
from tgbot.handlers import echo_router, user_router, admin_router, group_router
from tgbot.handlers.core import core_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.development_mode import DevelopmentModeMiddleware
from tgbot.middlewares.language import ACLMiddleware
from tgbot.services import broadcaster


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(ContentType.TEXT, bot, admin_ids, "Бот був запущений")


def run_upgrade():
    try:
        config = alembic_config("alembic.ini")
        config.attributes['configure_logger'] = False

        logging.info("Starting database upgrade process")
        command.upgrade(config, "head")
        logging.info("Database upgrade completed successfully")

    except Exception as e:
        logging.error("An error occurred during database upgrade: %s", str(e))


def register_router(dp: Dispatcher):
    dp.include_router(core_router)

    for router in [
        group_router,
        admin_router,
        user_router,
    ]:
        dp.include_router(router)
    setup_all_dialogs(dp)
    dp.include_router(echo_router)


def register_scheduler_jobs(scheduler: AsyncIOScheduler, sqlalchemy_session_pool: async_sessionmaker, bot: Bot):
    data = SchedulerData(scheduler, sqlalchemy_session_pool, bot)
    schedule_jobs(data, scheduler)


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    middleware_types = [
        DevelopmentModeMiddleware(config),
        ConfigMiddleware(config),
        DatabaseMiddleware(session_pool),
        ACLMiddleware(i18n)
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    config = load_config(".env")
    storage = get_storage(config)
    openai.api_key = config.misc.openai_api_key
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler(timezone=pytz.UTC)
    register_router(dp)
    engine = create_engine(config.db)
    sqlalchemy_session_pool = create_session_pool(engine)
    await seed_data(sqlalchemy_session_pool)
    register_global_middlewares(dp, config, session_pool=sqlalchemy_session_pool)
    register_scheduler_jobs(scheduler, sqlalchemy_session_pool, bot)

    scheduler.start()
    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        setup_logging()
        run_upgrade()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
