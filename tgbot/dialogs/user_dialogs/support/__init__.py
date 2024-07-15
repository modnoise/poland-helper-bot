from aiogram_dialog import Dialog

from . import windows


def support_dialogs():
    return [
        Dialog(
            windows.support_question_window(),
            windows.last_checked_question_window(),
        )
    ]