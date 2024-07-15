from aiogram_dialog import Dialog
from . import windows


def ai_queries_dialogs():
    return [
        Dialog(
            windows.ask_username_or_id(),
            windows.info_available_queries(),
            windows.input_queries_quantity()
        ),
    ]
