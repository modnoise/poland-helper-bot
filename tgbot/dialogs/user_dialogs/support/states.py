from aiogram.fsm.state import StatesGroup, State


class Support(StatesGroup):
    get_question = State()
    last_checked_question = State()