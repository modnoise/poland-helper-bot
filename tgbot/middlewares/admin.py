from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from domain import User
from tgbot.config import Config


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get('user')
        config: Config = data.get('config')
        if user.is_admin or event.from_user.id in config.tg_bot.admin_ids:
            return await handler(event, data)
