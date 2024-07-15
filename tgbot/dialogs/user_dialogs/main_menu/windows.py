from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format
from . import selected, states, keyboards, getters


def main_menu_window():
    return Window(
        Format("{text}"),
        keyboards.main_menu_keyboard(
            selected.on_feedback_click,
            selected.on_helper_click,
            selected.on_hub_click,
        ),
        state=states.MainMenu.start,
        getter=getters.main_menu_getter,
        disable_web_page_preview=True
    )

def deny_tools_access_window():
    return Window(
        Format("{text}"),
        Button(
            text=Format("{go_back}"),
            id="go_back",
            on_click=selected.goto_main_menu
        ),
        state=states.MainMenu.deny_tools_access,
        getter=getters.deny_tools_access_getter,
    )
