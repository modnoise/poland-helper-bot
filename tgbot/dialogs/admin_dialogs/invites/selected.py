from secrets import token_urlsafe
import re
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.admin_dialogs.invites.states import Invites
from tgbot.dialogs.admin_dialogs.menu_dialogs.states import AdminMenu


async def go_to_main_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AdminMenu.show_menu, mode=StartMode.RESET_STACK)


async def go_to_invites_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(Invites.show_menu, mode=StartMode.RESET_STACK)


async def on_rename_invite(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Invites.send_name_for_invite)


async def send_invites_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(Invites.show_menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)


async def on_enter_invite_name(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Invites.enter_invite_name)


async def on_generate_invite_click(message: Message, widget: TextInput, manager: DialogManager, invite_name: str):
    repo: RequestsRepo = manager.middleware_data.get("repo")
    code = token_urlsafe(6)
    await repo.invites.add_invite(code, invite_name)
    bot_data = await message.bot.me()
    invite_link = f"https://t.me/{bot_data.username}?start={code}"
    await message.answer("✅ <b>Посилання успішно згенеровано</b>\n\n"
                         f"<code>{invite_link}</code>")
    await manager.switch_to(Invites.show_menu, show_mode=ShowMode.SEND)


async def on_analytics_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Invites.send_invite_fot_analytics)


async def on_invites_list(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Invites.invites_list)


async def on_invite_editor(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Invites.invite_editor)


async def on_chosen_invite(message: Message, widget: TextInput, manager: DialogManager, invite_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(invite_id=int(invite_id))
    await manager.switch_to(Invites.invite_editor)


async def on_invite_analytic_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Invites.get_analytics_by_invite)


async def on_delete_invite(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Invites.confirm_delete_invite)


async def on_confirm_delete_invite(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    invite_id = ctx.dialog_data.get("invite_id")
    invite = await repo.invites.get_invite_by_id(invite_id)
    invite_name = invite.name if invite.name else invite.code

    await repo.invites.delete_invite_by_id(invite_id)
    await call.message.edit_text(
        text=f"🔗 Інвайт: <b>{invite_name}</b> - успішно видалено."
    )
    await manager.start(Invites.show_menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)


async def on_cancel_deleting_invite(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(Invites.show_menu, mode=StartMode.RESET_STACK)


async def on_change_invite_name(message: Message, widget: TextInput, manager: DialogManager, invite_name: str):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    invite_id = ctx.dialog_data.get("invite_id")
    await repo.invites.change_name_by_id(invite_name, invite_id)
    await manager.switch_to(Invites.invite_editor)


async def on_entered_invite_link(message: Message, widget: TextInput, manager: DialogManager, invite_link: str):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    bot_data = await message.bot.me()
    pattern = rf"https://t\.me/{bot_data.username}\?start=(\w+)"

    match = re.search(pattern, invite_link)

    if match:
        parse_code = match.group(1)
        code = await repo.invites.get_invite(parse_code)
        if code:
            ctx.dialog_data.update(invite_code=parse_code)
            await manager.switch_to(Invites.get_analytics_by_invite)
            return

        await message.answer(
            text="⚠️ <b>Вибачте, але посилання з таким кодом не знайдено.</b>\n\n"
                 "Будь ласка, перевірте його та спробуйте знову."
        )
        return

    await message.answer(
        text="⚠️ <b>Вибачте, але виглядає, що ви ввели неправильне посилання. Будь ласка, спробуйте знову.</b>"
    )
