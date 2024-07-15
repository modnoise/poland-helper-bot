import logging

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram.utils.i18n import gettext as _

from tgbot.dialogs.user_dialogs.connect_hub.states import ConnectHub
from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu


async def goto_main_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(MainMenu.start, mode=StartMode.RESET_STACK)


async def goto_connect_hub_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(ConnectHub.menu)


async def on_search_expert_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(ConnectHub.request_for_expert)


async def on_provide_questionnaire_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(ConnectHub.provide_questionnaire)


async def on_entered_request(message: Message, widget: TextInput, manager: DialogManager, request: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(request=request)
    await manager.switch_to(ConnectHub.request_confirmation)


async def on_confirmation_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    bot: Bot = manager.middleware_data.get("bot")
    request = ctx.dialog_data.get("request")
    telegram_id = call.from_user.id
    user_fullname = f'<a href="tg://user?id={telegram_id}">{call.from_user.full_name}</a>'
    username = f"@{call.from_user.username}"
    prefix = f"{user_fullname}, {username} (#ID{telegram_id})"

    try:
        await bot.send_message(
            chat_id=-4124710410,
            text=f"<b>Запит на експерта</b> 🕵️‍♂️🔍\n\n"
                 f"{request}\n\n"
                 f"{prefix}"
        )
    except Exception as e:
        logging.error(e)

    text = _("Your request has been sent.\n"
             "⏱ Please wait for a reply.")
    await call.message.edit_text(text=text)
    await manager.start(ConnectHub.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)


async def on_questionnaire_confirmation_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    bot: Bot = manager.middleware_data.get("bot")
    questionnaire = ctx.dialog_data.get("questionnaire")
    telegram_id = call.from_user.id
    user_fullname = f'<a href="tg://user?id={telegram_id}">{call.from_user.full_name}</a>'
    username = f"@{call.from_user.username}"
    prefix = f"{user_fullname}, {username} (#ID{telegram_id})"

    try:
        await bot.send_message(
            chat_id=-4124710410,
            text=f"<b>Нова анкета Експерта</b> 📝\n\n"
                 f"{questionnaire}\n\n"
                 f"{prefix}"
        )
    except Exception as e:
        logging.error(e)

    text = _("Thank you for filling out the questionnaire! We will contact you about further cooperation.")
    await call.message.edit_text(text=text)
    await manager.start(ConnectHub.menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)


async def on_entered_questionnaire(message: Message, widget: TextInput, manager: DialogManager, questionnaire: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(questionnaire=questionnaire)
    await manager.switch_to(ConnectHub.questionnaire_confirmation)