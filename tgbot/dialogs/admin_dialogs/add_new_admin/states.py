from aiogram.fsm.state import StatesGroup, State


class AddNewAdmin(StatesGroup):
    ask_username_or_telegram_id = State()
    confirm_choose = State()