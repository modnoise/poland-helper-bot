from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def payment_keyboard(payment_link: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Pay"),
        url=payment_link
    )
    return builder.as_markup()
