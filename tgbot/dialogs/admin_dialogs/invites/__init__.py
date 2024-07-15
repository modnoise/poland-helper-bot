from aiogram_dialog import Dialog
from . import windows


def invites_dialogs():
    return [
        Dialog(
            windows.invites_menu_window(),
            windows.generate_invite(),
            windows.invites_list(),
            windows.invite_editor(),
            windows.confirm_delete_invite(),
            windows.send_name_for_invite(),
            windows.send_invite_fot_analytics_window(),
            windows.get_analytics_by_invite_window(),
        )
    ]