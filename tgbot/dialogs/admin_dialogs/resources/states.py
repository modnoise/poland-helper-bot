from aiogram.fsm.state import StatesGroup, State


class Resources(StatesGroup):
    library = State()
    edit_library_url = State()