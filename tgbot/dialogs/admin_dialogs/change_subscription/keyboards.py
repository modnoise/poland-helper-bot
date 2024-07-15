from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Const


def change_subscription_menu_keyboard(on_edit_user_subscription):
    return Group(
        Button(
            text=Const("Редагувати для користувача ✏️"),
            on_click=on_edit_user_subscription,
            id="b_eus"
        )
    )


def info_user_subscription_keyboard(on_last_check_before_edit_user):
    return Group(
        Button(
            text=Const("Надати підписку 🔑"),
            on_click=on_last_check_before_edit_user,
            id="b_ps",
            when="provide_subscription"
        ),
        Button(
            text=Const("Скасувати підписку 🔒"),
            on_click=on_last_check_before_edit_user,
            id="b_cs",
            when="cancel_subscription"
        ),
    )


def last_check_before_edit_user_keyboard(on_confirm, on_cancelled):
    return Group(
        Button(
            text=Const("✅"),
            on_click=on_confirm,
            id="confirm"
        ),
        Button(
            text=Const("❌"),
            on_click=on_cancelled,
            id="cancel"
        ),
        width=2
    )
