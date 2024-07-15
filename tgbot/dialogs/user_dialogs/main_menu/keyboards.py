from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Format, Const


def main_menu_keyboard(on_feedback_click, on_helper_click, on_hub_click):
    return Group(
        Button(
            text=Format("{poland_helper_button_text}"),
            id="helper",
            on_click=on_helper_click
        ),
        Button(
            text=Format("{find_expert_button_text}"),
            id="hub",
            on_click=on_hub_click
        ),
        Button(
            text=Format("{feedback_button_text}"),
            id="feedback",
            on_click=on_feedback_click
        ),
    )
