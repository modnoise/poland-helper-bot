from datetime import datetime
from typing import Union

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu
from tgbot.dialogs.user_dialogs.payment.states import PaymentDialogs
from tgbot.keyboards.inline.callback_data import UpdateTariffPlanData
from tgbot.keyboards.inline.callback_data.profile_data import ProfileData

profile_router = Router()


@profile_router.message(Command("profile"))
@profile_router.callback_query(ProfileData.filter())
async def send_profile_info(message: Union[Message, CallbackQuery], dialog_manager: DialogManager):
    if isinstance(message, CallbackQuery):
        call = message
        await call.message.delete_reply_markup()

    await dialog_manager.start(MainMenu.profile, mode=StartMode.RESET_STACK)


@profile_router.callback_query(UpdateTariffPlanData.filter())
async def send_profile_info(call: CallbackQuery, dialog_manager: DialogManager):
    await dialog_manager.start(PaymentDialogs.payment_info, mode=StartMode.RESET_STACK)
