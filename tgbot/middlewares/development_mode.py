from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject

from tgbot.config import Config


class DevelopmentModeMiddleware(BaseMiddleware):
    def __init__(self, config: Config) -> None:
        self.config = config

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> None:
        bot: Bot = data.get('bot')

        if self.config.tg_bot.environment == 'DEVELOPMENT':
            if event.from_user.id in self.config.tg_bot.admin_ids:
                return await handler(event, data)
            else:
                await bot.send_message(
                    chat_id=event.from_user.id,
                    text="We're sorry for the inconvenience, but our bot is temporarily down due to maintenance. "
                         "Thank you for your patience and understanding. 😊🙏"
                )
        else:
            return await handler(event, data)
