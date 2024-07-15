from typing import Union

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from tgbot.dialogs.user_dialogs.support.states import Support
from tgbot.keyboards.inline.callback_data import SupportData

user_support_router = Router()


@user_support_router.message(Command("support"))
@user_support_router.callback_query(SupportData.filter())
async def ask_question(message: Union[Message, CallbackQuery], state: FSMContext, dialog_manager: DialogManager):
    await state.clear()
    if isinstance(message, CallbackQuery):
        call = message
        await call.message.delete_reply_markup()

    await dialog_manager.start(Support.get_question, mode=StartMode.RESET_STACK)