from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format
from . import selected, states, getters


def support_question_window():
    return Window(
        Format("{text}"),
        TextInput(
            id="q_id",
            on_success=selected.on_entered_question
        ),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_main_menu
        ),
        getter=getters.get_message_support,
        state=states.Support.get_question
    )


def last_checked_question_window():
    return Window(
        Format("{text}"),
        Row(
            Button(
                text=Const("✅"),
                on_click=selected.on_confirm,
                id="confirm_q"
            ),
            Button(
                text=Const("❌"),
                on_click=selected.on_cancelled,
                id="cancel_q"
            ),
        ),
        getter=getters.get_user_question,
        state=states.Support.last_checked_question
    )
