import datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import StartMode, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from application.core.enums import SubscriptionType
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.admin_dialogs.change_subscription.states import ChangeSubscription
from tgbot.dialogs.admin_dialogs.menu_dialogs.states import AdminMenu


async def go_to_main_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AdminMenu.show_menu, mode=StartMode.RESET_STACK)


async def go_to_change_subscription_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(ChangeSubscription.change_subscription_menu)


async def on_edit_user_subscription(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(ChangeSubscription.get_user_to_edit_subscription)


async def on_entered_username_or_id(message: Message, widget: TextInput, manager: DialogManager, result_input: str):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    result = result_input.split(' ')
    admin_telegram_id = message.from_user.id

    if len(result) > 1:
        await message.answer("⚠️ <b>Я очікував від тебе лише Username або ID, а не декілька значень.</b>")
    else:
        if result[0].isdigit():
            user = await repo.users.get_user(telegram_id=int(result[0]))
        else:
            user = await repo.users.get_user(username=result[0])

        if user:
            if (user.is_admin and user.telegram_id == admin_telegram_id) or not user.is_admin:
                ctx.dialog_data.update(user_telegram_id=user.telegram_id)
                await manager.switch_to(ChangeSubscription.info_user_subscription)
                return
            else:
                await message.answer(
                    "⚠️ <b>Користувач з цим Telegram ID є адміном, ви не можете редагувати його підписку.</b>")
        else:
            await message.answer("⚠️ <b>Користувача з цим Telegram ID або Username - не знайдено.</b>")
        await manager.switch_to(ChangeSubscription.get_user_to_edit_subscription)


async def on_last_check_before_edit_user(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(ChangeSubscription.last_check_before_edit_user)


async def on_confirm_edit_subscription(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    user_telegram_id = ctx.dialog_data.get('user_telegram_id')
    user = await repo.users.get_user(telegram_id=user_telegram_id)

    if user.subscription_detail:
        await repo.subscription.cancel_subscription(user.id)
    else:
        await repo.subscription.update_subscription(SubscriptionType.STANDARD, user.id)

    await manager.switch_to(ChangeSubscription.info_user_subscription)
