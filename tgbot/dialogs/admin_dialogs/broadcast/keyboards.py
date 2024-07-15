import operator

from aiogram_dialog.widgets.kbd import Group, Button, Select, Row
from aiogram_dialog.widgets.text import Const, Format


def language_keyboard(on_click):
    return Select(
            Format("{item[0]}"),
            id="s_lang",
            item_id_getter=operator.itemgetter(1),
            items="langs",
            on_click=on_click
        )


def choose_audience_type_keyboard(on_click):
    return Group(
        Select(
            Format("{item[0]}"),
            id="s_audience",
            item_id_getter=operator.itemgetter(1),
            items="audiences",
            on_click=on_click
        ),
        width=1
    )


def edit_message_keyboard(edit_message, delete_media, delete_text, launch_broadcast):
    return Group(
        Button(
            text=Const("Редагувати"),
            on_click=edit_message,
            id="edit_message"
        ),
        Button(
            text=Const("Видалити медія"),
            on_click=delete_media,
            id="delete_media",
            when="media"
        ),
        Button(
            text=Const("Видалити текст"),
            on_click=delete_text,
            id="delete_text",
            when="text"
        ),
        Button(
            text=Const("Відправити 📩"),
            on_click=launch_broadcast,
            id="launch_broadcast"
        )
    )


def last_check_keyboard(launch_broadcast, on_cancel):
    return Row(
        Button(
            text=Const("✅"),
            on_click=launch_broadcast,
            id="launch_broadcast"
        ),
        Button(
            text=Const("❌"),
            on_click=on_cancel,
            id="cancel_broadcast"
        ),
    )
