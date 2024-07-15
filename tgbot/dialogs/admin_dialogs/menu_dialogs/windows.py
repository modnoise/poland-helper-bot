from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Back, Button
from aiogram_dialog.widgets.text import Format, Const
from . import keyboards, selected, states, getters
from ..global_selected import go_to_main_menu


def main_menu_window():
    return Window(
        Format("{text}"),
        keyboards.main_menu_list(
            selected.go_to_add_admin,
            selected.go_to_ai_queries,
            selected.go_to_statistics,
            selected.go_to_broadcast,
            selected.on_invites_click,
        ),
        state=states.AdminMenu.show_menu,
        getter=getters.get_main_menu,
    )


def statistics_window():
    return Window(
        Format("{text}"),
        Back(Const("« Назад")),
        state=states.AdminMenu.show_statistics,
        getter=getters.get_statistics,
    )


def select_resource_window():
    return Window(
        Const("Обери ресурс який тебе цікавить 👇"),
        keyboards.select_resource_keyboard(
            selected.on_library_resource_click,
        ),
        Button(
            text=Const("« Назад"),
            on_click=go_to_main_menu,
            id="go_main"
        ),
        state=states.AdminMenu.select_resource,
    )