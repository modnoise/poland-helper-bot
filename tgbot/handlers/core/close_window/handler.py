from aiogram import Router
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline.callback_data import CloseData

close_router = Router()


@close_router.callback_query(CloseData.filter())
async def start_consultation(call: CallbackQuery):
    await call.message.delete()
