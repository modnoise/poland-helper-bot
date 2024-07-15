from aiogram.filters import BaseFilter
from aiogram.types import Message

from domain import User
from tgbot.config import Config


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, user: User, config: Config) -> bool:
        return (obj.from_user.id in config.tg_bot.admin_ids or user.is_admin) == self.is_admin
