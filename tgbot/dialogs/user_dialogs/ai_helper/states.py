from aiogram.fsm.state import StatesGroup, State


class AIHelper(StatesGroup):
    choose_role = State()
    role_details = State()
    start_conversational = State()
    how_to_use = State()
