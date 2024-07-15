from aiogram_dialog import Dialog
from . import windows


def main_menu_dialogs():
    return [
        Dialog(
            windows.main_menu_window(),
            windows.deny_tools_access_window(),
        )
    ]