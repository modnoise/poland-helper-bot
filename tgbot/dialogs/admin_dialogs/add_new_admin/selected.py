from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from domain import User
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.admin_dialogs.add_new_admin.states import AddNewAdmin
from tgbot.dialogs.admin_dialogs.menu_dialogs.states import AdminMenu


async def go_to_ask_admin_into(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(AddNewAdmin.ask_username_or_telegram_id)


async def on_entered_username_or_id(message: Message, widget: TextInput, manager: DialogManager, result_input: str):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    result = result_input.split(' ')
    if len(result) > 1:
        await message.answer("⚠️ <b>Я очікував від тебе лише Username або ID, а не декілька значень.</b>")
        await manager.switch_to(AddNewAdmin.ask_username_or_telegram_id)
        return

    if result[0].isdigit():
        user = await repo.users.get_user(telegram_id=int(result[0]))
        if user:
            ctx.dialog_data.update(admin_telegram_id=int(result[0]), admin_username=None)
            await manager.switch_to(AddNewAdmin.confirm_choose)
            return

        await message.answer("⚠️ <b>Користувача з цим Telegram ID - не знайдено.</b>")
        await manager.switch_to(AddNewAdmin.ask_username_or_telegram_id)
        return

    user = await repo.users.get_user(username=result[0])
    if user:
        ctx.dialog_data.update(admin_username=result[0], admin_telegram_id=None)
        await manager.switch_to(AddNewAdmin.confirm_choose)
        return
    await message.answer("⚠️ <b>Користувача з цим Username - не знайдено.</b>")
    await manager.switch_to(AddNewAdmin.ask_username_or_telegram_id)


async def on_confirm_added(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    admin_telegram_id = ctx.dialog_data.get('admin_telegram_id')
    admin_username = ctx.dialog_data.get('admin_username')

    user = None
    if admin_username:
        user = await repo.users.get_user(username=admin_username)
        await repo.users.add_admin(username=admin_username)

    if admin_telegram_id:
        user = await repo.users.get_user(telegram_id=admin_telegram_id)
        await repo.users.add_admin(telegram_id=admin_telegram_id)

    await call.message.edit_text(f"<b>Ви надали права адміністатора <code>{user.full_name}</code> ✅</b>")
    await manager.reset_stack()
    await manager.start(AdminMenu.show_menu)

