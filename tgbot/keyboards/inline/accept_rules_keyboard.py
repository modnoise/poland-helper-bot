from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data import AcceptRulesData


def accept_rules_keyboard(locale: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("I accept", locale=locale),
        callback_data=AcceptRulesData()
    )
    builder.adjust(1)
    return builder.as_markup()