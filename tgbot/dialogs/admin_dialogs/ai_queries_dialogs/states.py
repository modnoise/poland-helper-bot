from aiogram.fsm.state import State, StatesGroup


class AIQueries(StatesGroup):
    get_user = State()
    info_available_queries = State()
    enter_limit = State()
