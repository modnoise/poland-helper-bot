from aiogram_dialog import Dialog
from . import windows


def broadcast_dialogs():
    return [
        Dialog(
            windows.main_menu_window(),
            windows.choose_language_window(),
            windows.choose_auditory_type_window(),
            windows.message_edit_window(),
            windows.last_check_window()
        ),
    ]