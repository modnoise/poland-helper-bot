from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def greeting_video_note_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Next"),
        callback_data="bonus_1"
    )
    return builder.as_markup()