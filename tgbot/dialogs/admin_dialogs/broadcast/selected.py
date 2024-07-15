import asyncio

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, BaseDialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select

from application.core.enums import AudienceBroadcastType
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.admin_dialogs.broadcast.states import BroadcastMenu
from tgbot.services.broadcaster import broadcast, get_execution_time_str_format


async def on_chosen_lang(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(lang=item_id)
    await manager.switch_to(BroadcastMenu.choose_audience_type)


async def on_chosen_audience(call: CallbackQuery, widget: Select, manager: DialogManager, audience_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(audience_id=int(audience_id))
    await manager.switch_to(BroadcastMenu.ask_message)


async def go_to_choose_language(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(BroadcastMenu.choose_language)


async def go_to_chose_audience(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(BroadcastMenu.choose_audience_type)


async def go_to_last_check(call: CallbackQuery, widget: Button, manager: DialogManager):
    await call.message.delete_reply_markup()
    manager.show_mode = ShowMode.SEND
    await manager.switch_to(BroadcastMenu.last_check_message)


async def got_base_message(message: Message, dialog: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    if message.photo:
        ctx.dialog_data.update(photo_id=message.photo[0].file_id,
                               video_id=None,
                               document_id=None)

    if message.video:
        ctx.dialog_data.update(video_id=message.video.file_id,
                               photo_id=None,
                               document_id=None)

    if message.document:
        ctx.dialog_data.update(document_id=message.document.file_id,
                               photo_id=None,
                               video_id=None)

    if message.text or message.caption:
        ctx.dialog_data.update(text=message.html_text)

    await manager.switch_to(BroadcastMenu.edit_message)


async def go_to_broadcast_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(BroadcastMenu.edit_message)


async def go_to_ask_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    lang = ctx.dialog_data.get('lang')
    ctx.dialog_data.clear()
    ctx.dialog_data.update(lang=lang)
    await manager.switch_to(BroadcastMenu.ask_message)


async def edit_message(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(edit_mode=True)
    await call.message.delete_reply_markup()
    manager.show_mode = ShowMode.SEND
    await manager.switch_to(BroadcastMenu.ask_message)


async def delete_media(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(
        document_id=None,
        video_id=None,
        photo_id=None
    )
    text = ctx.dialog_data.get("text")
    if text:
        await manager.switch_to(BroadcastMenu.edit_message)
        return

    ctx.dialog_data.update(edit_mode=False)
    await manager.switch_to(BroadcastMenu.ask_message)


async def delete_text(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update(
        text=None,
    )
    photo_id = ctx.dialog_data.get('photo_id')
    video_id = ctx.dialog_data.get('video_id')
    document_id = ctx.dialog_data.get('document_id')

    if photo_id or video_id or document_id:
        await manager.switch_to(BroadcastMenu.edit_message)
        return

    ctx.dialog_data.update(edit_mode=False)
    await manager.switch_to(BroadcastMenu.ask_message)


async def launch_broadcast(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    lang_code = ctx.dialog_data.get('lang')
    audience_id = ctx.dialog_data.get('audience_id')
    audience_type = AudienceBroadcastType(audience_id)

    repo: RequestsRepo = manager.middleware_data.get("repo")
    bot: Bot = manager.middleware_data.get("bot")

    users = await repo.users.get_users_for_broadcast(lang_code, audience_type)
    content_type = ContentType.TEXT

    photo_id = ctx.dialog_data.get('photo_id')
    video_id = ctx.dialog_data.get('video_id')
    document_id = ctx.dialog_data.get('document_id')
    text = ctx.dialog_data.get('text')
    media_id = None
    language = None
    audience_text = ""

    await manager.done()

    if lang_code == 'en':
        language = "англомовної"
    if lang_code == 'uk':
        language = "україномовної"
    if lang_code == 'ru':
        language = "російськомовної"

    if audience_type == AudienceBroadcastType.HAVE_SUBSCRIPTION:
        audience_text = ", яка має підписку"
    if audience_type == AudienceBroadcastType.HAVE_NOT_SUBSCRIPTION:
        audience_text = ", яка не має підписки"

    if photo_id:
        content_type = ContentType.PHOTO
        media_id = photo_id
    elif video_id:
        content_type = ContentType.VIDEO
        media_id = video_id
    elif document_id:
        content_type = ContentType.DOCUMENT
        media_id = document_id

    await call.message.edit_text(f"Запущено розсилку для {language} аудиторії{audience_text} 🚀.")
    start_time = asyncio.get_running_loop().time()
    counter = await broadcast(content_type, bot, users, text, media_id)
    end_time = asyncio.get_running_loop().time()
    execution_time, unit = get_execution_time_str_format(end_time - start_time)

    message = (
        f"Розсилку для <b>{language} аудиторії</b> успішно завершено 👌\n\n"
        f"<i>Усього: {counter}</i>\n"
        f"<i>Час виконання: {execution_time} {unit}</i>"
    )
    await call.message.answer(text=message)
