from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callback_data.confirm_data import ConfirmData


def confirm_keyboard(role_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅",
        callback_data=ConfirmData(result=True, role_id=role_id)
    )
    builder.button(
        text="❌",
        callback_data=ConfirmData(result=False, role_id=role_id)
    )
    builder.adjust(2)
    return builder.as_markup()