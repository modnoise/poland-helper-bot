from aiogram_dialog import Dialog
from . import windows


def ai_helper_dialogs():
    return [
        Dialog(
            windows.choose_role_window(),
            windows.role_details(),
            windows.start_conversational_window(),
            windows.how_to_use_window(),
        ),
    ]