from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data import SupportData, MenuData


def support_keyboard(main_menu: bool = False):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Support"),
        callback_data=SupportData()
    )
    if main_menu:
        builder.button(
            text=_("Menu"),
            callback_data=MenuData()
        )
    builder.adjust(1)
    return builder.as_markup()