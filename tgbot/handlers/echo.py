from aiogram import Router, F
from aiogram.utils.i18n import gettext as _
from aiogram.filters import StateFilter
from aiogram.types import Message

from tgbot.filters.chat_types import IsChat

echo_router = Router()
echo_router.message.filter(IsChat())
echo_router.callback_query.filter(IsChat())


@echo_router.message(StateFilter(None), F.successful_payment == None)
async def handle_spam(message: Message):
    text = _("Friend, I am still working on opening new features.")
    await message.answer(text=text)
