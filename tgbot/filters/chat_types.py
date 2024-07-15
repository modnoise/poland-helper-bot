from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class IsGroup(BaseFilter):
    async def __call__(self, obj: Union[CallbackQuery, Message]) -> bool:
        chat = None
        if isinstance(obj, Message):
            chat = obj.chat
        if isinstance(obj, CallbackQuery):
            chat = obj.message.chat
        return chat.type in ("group", "supergroup")


class IsChat(BaseFilter):
    async def __call__(self, obj: Union[CallbackQuery, Message]) -> bool:
        chat = None
        if isinstance(obj, Message):
            chat = obj.chat
        if isinstance(obj, CallbackQuery):
            chat = obj.message.chat
        return chat.type == "private"
