from aiogram_dialog import Dialog
from . import windows


def connect_hub_dialogs():
    return [
        Dialog(
            windows.menu_window(),
            windows.request_for_expert_window(),
            windows.request_confirmation_window(),
            windows.provide_questionnaire_window(),
            windows.questionnaire_confirmation_window(),
        ),
    ]
