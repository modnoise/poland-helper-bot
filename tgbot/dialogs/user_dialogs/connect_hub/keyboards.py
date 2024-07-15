from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Format


def menu_keyboard(on_search_expert_click, on_provide_questionnaire_click):
    return Group(
        Button(
            text=Format("{search_expert_button_text}"),
            on_click=on_search_expert_click,
            id="b_se"
        ),
        Button(
            text=Format("{provide_questionnaire_button_text}"),
            on_click=on_provide_questionnaire_click,
            id="b_pq"
        )
    )