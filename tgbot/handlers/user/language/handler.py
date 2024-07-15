from aiogram import Router, Bot
from aiogram.utils.i18n import gettext as _
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from domain import User
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.commands.user_commands import set_user_start_commands
from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu
from tgbot.handlers.user.language.utils import send_lang_keyboard
from tgbot.keyboards.inline.callback_data.language_data import LanguageData
from tgbot.states import SetLanguage

language_router = Router()


@language_router.message(Command("language"))
async def ask_language(message: Message, bot: Bot, state: FSMContext):
    telegram_id = message.from_user.id
    await send_lang_keyboard(bot, telegram_id)
    await state.set_state(SetLanguage.get_lang)


@language_router.message(StateFilter(SetLanguage.get_lang))
async def handle_spam(message: Message):
    await message.delete()


@language_router.callback_query(StateFilter(SetLanguage.get_lang), LanguageData.filter())
async def ask_language(call: CallbackQuery,
                       bot: Bot,
                       state: FSMContext,
                       callback_data: LanguageData,
                       repo: RequestsRepo,
                       user: User,
                       dialog_manager: DialogManager):
    await repo.users.set_language(callback_data.lang, user.id)
    text = _("👌 <b>language is selected.</b>\n\n"
             "<i>To change the language, use the command:</i> /language", locale=callback_data.lang)
    await call.message.edit_text(text=text)
    await set_user_start_commands(
        chat_id=user.telegram_id,
        bot=bot,
        lang=callback_data.lang
    )
    await state.clear()
    await dialog_manager.reset_stack()
    await dialog_manager.start(MainMenu.start, mode=StartMode.RESET_STACK)
