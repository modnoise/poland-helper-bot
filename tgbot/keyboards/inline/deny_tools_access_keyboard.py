from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data.info_center_data import InfoCenterData
from tgbot.keyboards.inline.callback_data.profile_data import ProfileData


def deny_tools_access_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Profile 👤"),
        callback_data=ProfileData()
    )
    builder.button(
        text=_("Back ↩️"),
        callback_data=InfoCenterData()
    )
    builder.adjust(1)
    return builder.as_markup()