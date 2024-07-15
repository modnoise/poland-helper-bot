from aiogram import Router

from tgbot.handlers.core.close_window import close_router

core_router = Router()

for router in [
    close_router,
]:
    core_router.include_router(router)
