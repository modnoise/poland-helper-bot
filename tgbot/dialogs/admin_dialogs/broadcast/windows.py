from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from . import getters, states, selected, keyboards
from ..global_selected import go_to_main_menu


def choose_language_window():
    return Window(
        Const("Обери мову аудиторії"),
        keyboards.language_keyboard(selected.on_chosen_lang),
        Button(
            text=Const("« Назад"),
            on_click=go_to_main_menu,
            id="go_main",
        ),
        getter=getters.get_langs_to_choose,
        state=states.BroadcastMenu.choose_language
    )


def choose_auditory_type_window():
    return Window(
        Const("Обери аудиторію"),
        keyboards.choose_audience_type_keyboard(selected.on_chosen_audience),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_choose_language,
            id="go_main",
        ),
        getter=getters.choose_audience_type_getter,
        state=states.BroadcastMenu.choose_audience_type
    )


def main_menu_window():
    return Window(
        Format("{text}"),
        MessageInput(content_types=[ContentType.VIDEO, ContentType.PHOTO, ContentType.DOCUMENT, ContentType.TEXT],
                     func=selected.got_base_message),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_chose_audience,
            id="select_audience",
            when="s_audience"
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_broadcast_menu,
            id="go_edit",
            when="go_to_edit_menu"
        ),
        getter=getters.get_text_to_ask_message,
        state=states.BroadcastMenu.ask_message,
    )


def message_edit_window():
    return Window(
        DynamicMedia(
            selector="media",
            when="media"
        ),
        Format("{text}", when="text"),
        keyboards.edit_message_keyboard(
            selected.edit_message,
            selected.delete_media,
            selected.delete_text,
            selected.go_to_last_check
        ),
        Row(
            Button(
                text=Const("« Назад"),
                on_click=selected.go_to_ask_menu,
                id="go_brd_menu"
            ),
            Button(
                text=Const("Скинути 🗑️"),
                on_click=go_to_main_menu,
                id="cancel",
            )
        ),
        getter=getters.get_message,
        state=states.BroadcastMenu.edit_message,
        disable_web_page_preview=True,
    )


def last_check_window():
    return Window(
        Format("{text}"),
        keyboards.last_check_keyboard(selected.launch_broadcast, go_to_main_menu),
        getter=getters.get_last_check_text,
        state=states.BroadcastMenu.last_check_message,
        disable_web_page_preview=True,
    )