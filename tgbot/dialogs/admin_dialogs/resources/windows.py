from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const
from . import keyboards, selected, states, getters
from ..global_selected import go_to_select_resources


def library_window():
    return Window(
        Format("{text}"),
        Button(
            text=Const("Редагувати посилання 🔗"),
            on_click=selected.on_edit_library_url_click,
            id="elu"
        ),
        Button(
            text=Const("« Назад"),
            on_click=go_to_select_resources,
            id="go_s_r"
        ),
        state=states.Resources.library,
        getter=getters.library_getters,
        disable_web_page_preview=True
    )


def edit_library_url_window():
    return Window(
        Const("Введіть нове посилання для <b>Life Library</b>"),
        TextInput(
            id="liburl",
            on_success=selected.on_entered_library_url
        ),
        Button(
            text=Const("« Назад"),
            on_click=go_to_select_resources,
            id="go_s_r"
        ),
        state=states.Resources.edit_library_url,
    )