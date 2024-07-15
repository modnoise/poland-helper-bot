from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format
from . import keyboards, selected, states, getters


def invites_menu_window():
    return Window(
        Const("Обери що тебе цікавить"),
        keyboards.invites_menu_keyboard(
            selected.on_enter_invite_name,
            selected.on_analytics_click,
            selected.on_invites_list
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_main_menu,
            id="go_main"
        ),
        state=states.Invites.show_menu
    )


def generate_invite():
    return Window(
        Const("Напиши ім'я для інвайту"),
        TextInput(
            id="t_i_ri",
            on_success=selected.on_generate_invite_click
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_invites_menu,
            id="go_i_l"
        ),
        state=states.Invites.enter_invite_name
    )


def invites_list():
    return Window(
        Const("Обери необхідний інвайт:"),
        keyboards.invites_list_keyboards(selected.on_chosen_invite),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_invites_menu,
            id="go_i_menu"
        ),
        state=states.Invites.invites_list,
        getter=getters.invites_list_getter
    )


def invite_editor():
    return Window(
        Format("{text}"),
        keyboards.invite_editor_keyboards(
            selected.on_invite_analytic_click,
            selected.on_delete_invite,
            selected.on_rename_invite
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.on_invites_list,
            id="go_i_list"
        ),
        state=states.Invites.invite_editor,
        getter=getters.invite_editor_getter
    )


def confirm_delete_invite():
    return Window(
        Format("{text}"),
        Row(
            Button(
                text=Const("✅"),
                on_click=selected.on_confirm_delete_invite,
                id="b_di"
            ),
            Button(
                text=Const("❌"),
                on_click=selected.on_cancel_deleting_invite,
                id="b_cdi"
            )
        ),
        state=states.Invites.confirm_delete_invite,
        getter=getters.confirm_delete_invite_getter
    )


def send_name_for_invite():
    return Window(
        Const("Напиши ім'я для інвайту"),
        TextInput(
            id="t_i_ri",
            on_success=selected.on_change_invite_name
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.on_invite_editor,
            id="go_i_l"
        ),
        state=states.Invites.send_name_for_invite
    )


def send_invite_fot_analytics_window():
    return Window(
        Const("Вібрав мені посилання, щоб отримати статистику."),
        TextInput(
            id="link",
            on_success=selected.on_entered_invite_link
        ),
        Button(
            text=Const("« Назад"),
            on_click=selected.go_to_invites_menu,
            id="go_i_menu"
        ),
        state=states.Invites.send_invite_fot_analytics
    )


def get_analytics_by_invite_window():
    return Window(
        Format("{text}"),
        Button(
            text=Const("« Назад"),
            on_click=selected.send_invites_menu,
            id="go_i_menu"
        ),
        state=states.Invites.get_analytics_by_invite,
        getter=getters.get_analytics_by_invite_getter
    )
