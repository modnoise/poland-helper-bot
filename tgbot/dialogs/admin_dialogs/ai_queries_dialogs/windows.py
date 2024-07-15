from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const
from . import getters, selected, keyboards, states


def ask_username_or_id():
    return Window(
        Const("Введи Username або Telegram ID:"),
        TextInput(
            id="usr_id",
            on_success=selected.on_entered_username_or_id
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_back_to_menu,
            id="go_menu"
        ),
        state=states.AIQueries.get_user,
    )


def info_available_queries():
    return Window(
        Format("{text}"),
        keyboards.increase_available_queries_menu(
            selected.on_increase_available_queries,
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_get_user,
            id="go_get_user"
        ),
        state=states.AIQueries.info_available_queries,
        getter=getters.get_limits_info
    )


def input_queries_quantity():
    return Window(
        Format("{text}"),
        TextInput(
            id="input_limit",
            on_success=selected.on_enter_limit
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_back_to_menu,
            id="go_limit_menu"
        ),
        state=states.AIQueries.enter_limit,
        getter=getters.get_text_for_input
    )
