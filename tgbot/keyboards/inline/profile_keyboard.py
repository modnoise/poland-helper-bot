from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data.profile_data import ProfileData


def profile_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Profile 👤"),
        callback_data=ProfileData()
    )
    return builder.as_markup()