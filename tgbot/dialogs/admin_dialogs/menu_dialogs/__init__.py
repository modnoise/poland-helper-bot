from aiogram_dialog import Dialog

from . import windows


def menu_dialogs():
    return [
        Dialog(
            windows.main_menu_window(),
            windows.statistics_window(),
            windows.select_resource_window(),
        )
    ]
