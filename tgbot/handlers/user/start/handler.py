import logging
from aiogram import Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from application.core.captcha import generate_captcha
from domain import User
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.commands.user_commands import set_user_defaults_commands, set_user_start_commands
from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu
from tgbot.handlers.user.language.utils import send_lang_keyboard, send_captcha
from tgbot.keyboards.inline.callback_data import MenuData
from tgbot.states import SetLanguage, Captcha

start_router = Router()


@start_router.message(CommandStart())
async def user_start(message: Message, bot: Bot, state: FSMContext, user: User, dialog_manager: DialogManager):
    telegram_id = message.from_user.id
    await state.clear()
    await dialog_manager.reset_stack(True)

    if not user.is_verify:
        await set_user_defaults_commands(telegram_id, bot)
        captcha_code, captcha_image = generate_captcha()
        captcha_message = await send_captcha(bot, telegram_id, captcha_image)
        await state.update_data(captcha_code=captcha_code, captcha_message_id=captcha_message.message_id)
        await state.set_state(Captcha.get_result)
        return

    if not user.language:
        await send_lang_keyboard(bot, user.telegram_id)
        await state.set_state(SetLanguage.get_lang)
        return

    if user.messages_limit == 0:
        return

    await set_user_start_commands(
        chat_id=telegram_id,
        bot=bot,
        lang=user.language
    )
    await dialog_manager.start(MainMenu.start, mode=StartMode.RESET_STACK)


@start_router.callback_query(MenuData.filter())
async def show_menu(call: CallbackQuery, state: FSMContext, dialog_manager: DialogManager):
    await state.clear()
    await call.message.delete_reply_markup()
    await dialog_manager.start(MainMenu.start, mode=StartMode.RESET_STACK)


@start_router.message(StateFilter(Captcha.get_result))
async def get_captcha_result(message: Message, bot: Bot, state: FSMContext, repo: RequestsRepo, user: User):
    telegram_id = message.from_user.id
    data = await state.get_data()
    captcha_code = data.get('captcha_code')
    captcha_message_id = data.get('captcha_message_id')

    if message.text == captcha_code:
        try:
            await bot.delete_message(telegram_id, captcha_message_id)
        except Exception as e:
            logging.error(e)
        await repo.users.set_verity(user.id, True)
        await repo.users.change_active(active=True)
        query_quantity = 300
        await repo.users.increase_available_queries_to_ai(user, query_quantity)
        await set_user_defaults_commands(
            chat_id=telegram_id,
            bot=bot
        )
        await send_lang_keyboard(bot, telegram_id)
        await state.set_state(SetLanguage.get_lang)
        return

    try:
        await bot.delete_message(telegram_id, captcha_message_id)
    except Exception as e:
        logging.error(e)
    captcha_code, captcha_image = generate_captcha()
    captcha_message = await send_captcha(bot, telegram_id, captcha_image)
    await state.update_data(captcha_code=captcha_code, captcha_message_id=captcha_message.message_id)
