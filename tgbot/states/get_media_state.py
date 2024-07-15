from aiogram.fsm.state import StatesGroup, State


class GetMedia(StatesGroup):
    get_file = State()
