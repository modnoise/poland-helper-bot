from aiogram.fsm.state import StatesGroup, State


class AdminMenu(StatesGroup):
    show_menu = State()
    show_statistics = State()
    select_resource = State()