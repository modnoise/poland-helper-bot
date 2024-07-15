from aiogram_dialog.widgets.kbd import Select, Group, Button
from aiogram_dialog.widgets.text import Const


def confirm_add_new_admin(on_confirm, on_cancelled):
    return Group(
        Button(
            text=Const("✅"),
            on_click=on_confirm,
            id="confirm"
        ),
        Button(
            text=Const("❌"),
            on_click=on_cancelled,
            id="cancel"
        ),
        width=2
    )