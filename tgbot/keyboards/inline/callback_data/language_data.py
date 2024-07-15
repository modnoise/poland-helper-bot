from aiogram.filters.callback_data import CallbackData


class LanguageData(CallbackData, prefix='lng'):
    lang: str