import logging
from aiogram.utils.i18n import gettext as _

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu
from tgbot.dialogs.user_dialogs.support.states import Support


async def goto_main_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(MainMenu.start, mode=StartMode.RESET_STACK)


async def on_entered_question(message: Message, widget: TextInput, manager: DialogManager, result_input: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(question=result_input)
    await manager.switch_to(Support.last_checked_question)


async def on_cancelled(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(Support.get_question)


async def on_confirm(call: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    bot: Bot = manager.middleware_data.get("bot")
    question = ctx.dialog_data.get("question")
    telegram_id = call.from_user.id
    user_fullname = f'<a href="tg://user?id={telegram_id}">{call.from_user.full_name}</a>'
    username = f"@{call.from_user.username}"
    prefix = f"{user_fullname}, {username} (#ID{telegram_id})"

    try:
        await bot.send_message(
            chat_id=-4124710410,
            text=f"{question}\n\n{prefix}"
        )
    except Exception as e:
        logging.error(e)

    text = _("Thank you for reaching out to us! "
             "Your request has been received, and our team is working diligently to assist you. "
             "We'll get back to you with a response as soon as possible. ")
    await call.message.edit_text(text=text)
    await manager.start(MainMenu.start, mode=StartMode.RESET_STACK, show_mode=ShowMode.SEND)
