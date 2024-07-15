from aiogram.fsm.state import StatesGroup, State


class BroadcastMenu(StatesGroup):
    ask_message = State()
    choose_language = State()
    choose_audience_type = State()
    edit_message = State()
    last_check_message = State()