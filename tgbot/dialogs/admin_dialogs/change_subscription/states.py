from aiogram.fsm.state import State, StatesGroup


class ChangeSubscription(StatesGroup):
    change_subscription_menu = State()
    get_user_to_edit_subscription = State()
    info_user_subscription = State()
    last_check_before_edit_user = State()
