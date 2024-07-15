from aiogram import Router

from tgbot.filters.chat_types import IsGroup
from tgbot.handlers.groups.support.handler import support_router

group_router = Router()

for router in [
    support_router,
]:
    group_router.include_router(router)

group_router.message.filter(IsGroup())
group_router.callback_query.filter(IsGroup())