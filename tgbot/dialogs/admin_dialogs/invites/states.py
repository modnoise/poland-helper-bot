from aiogram.fsm.state import StatesGroup, State


class Invites(StatesGroup):
    show_menu = State()
    send_invite_fot_analytics = State()
    enter_invite_name = State()
    get_analytics_by_invite = State()
    invites_list = State()
    invite_editor = State()
    confirm_delete_invite = State()
    send_name_for_invite = State()
