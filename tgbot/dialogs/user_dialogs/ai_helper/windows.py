from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format
from . import selected, states, keyboards, getters


def choose_role_window():
    return Window(
        Format("{text}"),
        keyboards.choose_role_keyboard(
            selected.on_select_role
        ),
        Row(
            Button(
                text=Format("{go_back}"),
                id="go_back",
                on_click=selected.goto_main_menu
            ),
            Button(
                text=Format("{details}"),
                id="b_dts",
                on_click=selected.on_role_details
            ),
        ),
        state=states.AIHelper.choose_role,
        getter=getters.choose_role_getter
    )


def role_details():
    return Window(
        Format("{text}"),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_choose_role
        ),
        state=states.AIHelper.role_details,
        getter=getters.role_details_getter
    )


def start_conversational_window():
    return Window(
        Format("{text}"),
        TextInput(
            id="question",
            on_success=selected.on_entered_question
        ),
        Button(
            text=Format("{how_to_use}"),
            id="b_htu",
            on_click=selected.goto_how_to_use
        ),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_choose_role
        ),
        state=states.AIHelper.start_conversational,
        getter=getters.start_conversational_getter,
        disable_web_page_preview=True
    )


def how_to_use_window():
    return Window(
        Format("{text}"),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_start_conversational
        ),
        state=states.AIHelper.how_to_use,
        getter=getters.how_to_use_window_getter,
        disable_web_page_preview=True
    )

