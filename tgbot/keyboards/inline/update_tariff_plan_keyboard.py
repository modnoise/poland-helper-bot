from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data import UpdateTariffPlanData


def update_tariff_plan_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Upgrade your tariff plan"),
        callback_data=UpdateTariffPlanData()
    )
    builder.adjust(1)
    return builder.as_markup()