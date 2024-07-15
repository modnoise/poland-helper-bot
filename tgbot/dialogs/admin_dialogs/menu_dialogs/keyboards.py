from aiogram_dialog.widgets.kbd import Column, Cancel, Button, Group, Row
from aiogram_dialog.widgets.text import Const


def main_menu_list(add_admin, ai_queries, show_statistics, launch_broadcast,
                   on_invites_click):
    return Group(
        Button(
            text=Const("Додати адміна 🛠️"),
            on_click=add_admin,
            id="addm"
        ),
        Row(
            Button(
                text=Const("Запити до AI 🔮"),
                on_click=ai_queries,
                id="chlt"
            ),
        ),
        Row(
            Button(
                text=Const("Статистика 📈"),
                on_click=show_statistics,
                id="stats"
            ),
            Button(
                text=Const("Розсилка 📩"),
                on_click=launch_broadcast,
                id="broadcast"
            )
        ),
        Button(
            text=Const("Інвайти 🔗"),
            on_click=on_invites_click,
            id="invites"
        ),
    )


def select_resource_keyboard(on_library_resource_click):
    return Group(
        Button(
            text=Const("Life Library"),
            on_click=on_library_resource_click,
            id="libres"
        ),
    )
