from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Const, Format


def increase_available_queries_menu(change_available_queries):
    return Group(
        Button(
            text=Format("{available_queries}"),
            on_click=change_available_queries,
            id='b_caq'
        ),
        width=1
    )
