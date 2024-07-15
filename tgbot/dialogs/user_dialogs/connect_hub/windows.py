from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Format, Const
from . import keyboards, selected, states, getters


def menu_window():
    return Window(
        Format("{text}"),
        keyboards.menu_keyboard(
            selected.on_search_expert_click,
            selected.on_provide_questionnaire_click,
        ),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_main_menu
        ),
        state=states.ConnectHub.menu,
        getter=getters.menu_getter,
    )


def request_for_expert_window():
    return Window(
        Format("{text}"),
        TextInput(
            id="request",
            on_success=selected.on_entered_request
        ),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_connect_hub_menu
        ),
        state=states.ConnectHub.request_for_expert,
        getter=getters.request_for_expert_getter,
    )


def request_confirmation_window():
    return Window(
        Format("{text}"),
        Row(

            Button(
                text=Const("✅"),
                id="confirm",
                on_click=selected.on_confirmation_click
            ),
            Button(
                text=Const("❌"),
                id="cancelled",
                on_click=selected.goto_connect_hub_menu
            )
        ),
        state=states.ConnectHub.request_confirmation,
        getter=getters.request_confirmation_getter,
    )


def provide_questionnaire_window():
    return Window(
        Format("{text}"),
        TextInput(
            id="questionnaire",
            on_success=selected.on_entered_questionnaire
        ),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_connect_hub_menu
        ),
        state=states.ConnectHub.provide_questionnaire,
        getter=getters.provide_questionnaire_getter,
    )


def questionnaire_confirmation_window():
    return Window(
        Format("{text}"),
        Row(
            Button(
                text=Const("✅"),
                id="confirm",
                on_click=selected.on_questionnaire_confirmation_click
            ),
            Button(
                text=Const("❌"),
                id="cancelled",
                on_click=selected.goto_connect_hub_menu
            )
        ),
        state=states.ConnectHub.questionnaire_confirmation,
        getter=getters.questionnaire_confirmation_getter,
    )