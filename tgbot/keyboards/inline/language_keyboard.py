from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.keyboards.inline.callback_data.language_data import LanguageData


def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="УКР",
        callback_data=LanguageData(lang="uk")
    )
    builder.button(
        text="ENG",
        callback_data=LanguageData(lang="en")
    )
    return builder.as_markup()