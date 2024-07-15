from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from . import states, selected, keyboards, getters
from tgbot.dialogs.admin_dialogs.global_selected import go_to_main_menu


def ask_username_or_id():
    return Window(
        Const("Введи Username або Telegram ID:"),
        TextInput(
            id="usr_id",
            on_success=selected.on_entered_username_or_id
        ),
        Button(
            text=Const("« Назад"),
            on_click=go_to_main_menu,
            id="go_main"
        ),
        state=states.AddNewAdmin.ask_username_or_telegram_id,
    )


def confirm_choose():
    return Window(
        Format("{text}"),
        keyboards.confirm_add_new_admin(selected.on_confirm_added, go_to_main_menu),
        state=states.AddNewAdmin.confirm_choose,
        getter=getters.get_check_info
    )