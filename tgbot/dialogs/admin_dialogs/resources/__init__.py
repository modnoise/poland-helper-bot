from aiogram_dialog import Dialog
from . import windows


def resources_dialogs():
    return [
        Dialog(
            windows.library_window(),
            windows.edit_library_url_window(),
        )
    ]
