from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    start = State()
    info_center_menu = State()
    profile = State()
    rules = State()
    support_request = State()
    confirmation_request = State()
    deny_tools_access = State()