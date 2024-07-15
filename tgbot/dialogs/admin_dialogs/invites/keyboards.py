import operator

from aiogram_dialog.widgets.kbd import Group, Button, ScrollingGroup, Select, Column
from aiogram_dialog.widgets.text import Const, Format


def invites_menu_keyboard(on_generate_invite_click, on_analytics_click, on_invite_list):
    return Group(
        Button(
            text=Const("Генерувати посилання 🪄"),
            on_click=on_generate_invite_click,
            id="b_gic"
        ),
        Button(
            text=Const("Аналітика 📊"),
            on_click=on_analytics_click,
            id="b_ac"
        ),
        Button(
            text=Const("Список 📃"),
            on_click=on_invite_list,
            id="b_il"
        ),
    )


def invites_list_keyboards(on_chosen_invite):
    return ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="s_scroll_invites",
            item_id_getter=operator.itemgetter(1),
            items="invites_data",
            on_click=on_chosen_invite
        ),
        id="invites_ids",
        width=1, height=5,
        hide_on_single_page=True
    )


def invite_editor_keyboards(
        on_invite_analytic_click,
        on_delete_invite,
        on_rename_invite):
    return Group(
        Button(
            text=Const("📊"),
            on_click=on_invite_analytic_click,
            id="b_ac"
        ),
        Button(
            text=Const("🗑️"),
            on_click=on_delete_invite,
            id="b_il"
        ),
        Button(
            text=Const("Перейменувати ✏️"),
            on_click=on_rename_invite,
            id="b_ri"
        ),
        width=2
    )
