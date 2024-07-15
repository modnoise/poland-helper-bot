from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data.clear_chat_data import ClearChatData


def consultation_keyboard(role_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Clear 🧹"),
        callback_data=ClearChatData(role_id=role_id)
    )
    builder.button(
        text=_("Menu 🏠"),
        callback_data="exit"
    )
    return builder.as_markup()