from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from . import selected, states, keyboards, getters


def change_subscription_menu():
    return Window(
        Const("Обери що тебе цікавить"),
        keyboards.change_subscription_menu_keyboard(selected.on_edit_user_subscription),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_main_menu,
            id="go_main"
        ),
        state=states.ChangeSubscription.change_subscription_menu
    )


def ask_username_or_id():
    return Window(
        Const("Введи Username або Telegram ID:"),
        TextInput(
            id="usr_id",
            on_success=selected.on_entered_username_or_id
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_change_subscription_menu,
            id="go_limit_menu"
        ),
        state=states.ChangeSubscription.get_user_to_edit_subscription,
    )


def info_user_subscription():
    return Window(
        Format("{text}"),
        keyboards.info_user_subscription_keyboard(
            selected.on_last_check_before_edit_user,
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_change_subscription_menu,
            id="go_main"
        ),
        getter=getters.info_user_subscription_getter,
        state=states.ChangeSubscription.info_user_subscription
    )


def last_check_before_edit_user():
    return Window(
        Format("{text}"),
        keyboards.last_check_before_edit_user_keyboard(
            selected.on_confirm_edit_subscription,
            selected.go_to_change_subscription_menu
        ),
        getter=getters.last_check_before_edit_user_getter,
        state=states.ChangeSubscription.last_check_before_edit_user
    )