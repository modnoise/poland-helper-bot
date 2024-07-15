from aiogram.fsm.state import StatesGroup, State


class SetLanguage(StatesGroup):
    get_lang = State()
