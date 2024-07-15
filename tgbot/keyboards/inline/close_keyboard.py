from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data import CloseData


def close_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("☑️ Сlose"),
        callback_data=CloseData()
    )
    return builder.as_markup()