from abc import ABC
from typing import Dict, Any

from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import I18nMiddleware
from domain import User


class ACLMiddleware(I18nMiddleware, ABC):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user: User = data.get('user')
        return user.language
