from aiogram_dialog import Dialog
from . import windows


def add_new_admin_dialogs():
    return [
        Dialog(
            windows.ask_username_or_id(),
            windows.confirm_choose(),
        ),
    ]
