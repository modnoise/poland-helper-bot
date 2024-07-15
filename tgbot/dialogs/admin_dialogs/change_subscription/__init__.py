from aiogram_dialog import Dialog
from . import windows


def change_subscription_dialogs():
    return [
        Dialog(
            windows.change_subscription_menu(),
            windows.ask_username_or_id(),
            windows.info_user_subscription(),
            windows.last_check_before_edit_user(),
        ),
    ]

