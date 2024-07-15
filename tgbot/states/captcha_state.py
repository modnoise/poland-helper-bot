from aiogram.fsm.state import StatesGroup, State


class Captcha(StatesGroup):
    get_result = State()
