from aiogram.filters.callback_data import CallbackData


class ClearChatData(CallbackData, prefix="ccd"):
    role_id: int