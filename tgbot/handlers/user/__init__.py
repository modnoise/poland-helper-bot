from aiogram import Router

from tgbot.filters.chat_types import IsChat
from tgbot.handlers.user.consultation import consultation_router
from tgbot.handlers.user.language import language_router
from tgbot.handlers.user.start import start_router
from tgbot.handlers.user.support import user_support_router
from tgbot.middlewares.authorization import AuthorizationMiddleware

user_router = Router()

for router in [
    start_router,
    language_router,
     user_support_router,
    consultation_router,
]:
    user_router.include_router(router)
    user_router.message.filter(IsChat())
    user_router.callback_query.filter(IsChat())

for router in [
    consultation_router,
]:
    router.message.outer_middleware(AuthorizationMiddleware())
    router.callback_query.outer_middleware(AuthorizationMiddleware())
