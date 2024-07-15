import operator

from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Format


def choose_role_keyboard(on_select_role):
    return Group(
        Select(
            Format("{item[0]}"),
            id="s_select_role",
            item_id_getter=operator.itemgetter(1),
            items="roles",
            on_click=on_select_role,
        ),
        width=1
    )
