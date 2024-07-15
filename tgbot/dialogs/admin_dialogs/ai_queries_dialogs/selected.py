import logging

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.admin_dialogs.ai_queries_dialogs.states import AIQueries
from tgbot.dialogs.admin_dialogs.menu_dialogs.states import AdminMenu


async def go_back_to_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AdminMenu.show_menu, mode=StartMode.RESET_STACK)

async def go_to_get_user(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AIQueries.get_user)


async def on_entered_username_or_id(message: Message, widget: TextInput, manager: DialogManager, result_input: str):
    ctx = manager.current_context()
    repo: RequestsRepo = manager.middleware_data.get("repo")
    result = result_input.split(' ')
    if len(result) > 1:
        await message.answer("⚠️ <b>Я очікував від тебе лише Username або ID, а не декілька значень.</b>")
        await manager.switch_to(AIQueries.get_user)
        return

    if result[0].isdigit():
        user = await repo.users.get_user(telegram_id=int(result[0]))
        if user:
            ctx.dialog_data.update(user_telegram_id=int(result[0]), user_username=None)
            await manager.switch_to(AIQueries.info_available_queries)
            return

        await message.answer("⚠️ <b>Користувача з цим Telegram ID - не знайдено.</b>")
        await manager.switch_to(AIQueries.get_user)
        return

    user = await repo.users.get_user(username=result[0])
    if user:
        ctx.dialog_data.update(user_telegram_id=None, user_username=result[0])
        await manager.switch_to(AIQueries.info_available_queries)
        return
    await message.answer("⚠️ <b>Користувача з цим Username - не знайдено.</b>")
    await manager.switch_to(AIQueries.get_user)


async def on_increase_available_queries(call: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(AIQueries.enter_limit)


async def on_enter_limit(message: Message, widget: TextInput, dialog_manager: DialogManager, result_input: str):
    ctx = dialog_manager.current_context()
    repo: RequestsRepo = dialog_manager.middleware_data.get("repo")
    bot: Bot = dialog_manager.middleware_data.get("bot")
    user_id = ctx.dialog_data.get("user_id")
    result = result_input.split(' ')
    if len(result) > 1:
        await message.answer("⚠️ <b>Я очікував від тебе лише число, а не декілька значень.</b>")
        await dialog_manager.switch_to(AIQueries.enter_limit)
        return

    if not result[0].isdigit():
        await message.answer(f"⚠️ <b>Я очікував від тебе число, а не <code>{result[0]}</code>.</b>")
        await dialog_manager.switch_to(AIQueries.enter_limit)
        return

    quantity = int(result[0])
    user = await repo.users.get_user(user_id)
    await repo.users.increase_available_queries_to_ai(
        user, quantity=quantity)

    try:
        if user.language == 'uk':
            text = f'🎉 Вашому акаунту нараховано додаткові {quantity} запитів до ШІ!'
        elif user.language == 'ru':
            text = f'🎉 Вашему аккаунту начислены дополнительные {quantity} запросов к ИИ!'
        else:
            text = f'🎉 Your account has been credited with additional {quantity} requests to AI!'

        await bot.send_message(chat_id=user.telegram_id,
                               text=text)
    except Exception as e:
        logging.error(e)

    await dialog_manager.switch_to(AIQueries.info_available_queries)
    return



