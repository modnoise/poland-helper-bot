from typing import Union

from aiogram.utils.i18n import gettext as _

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain import User
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.user_dialogs.ai_helper.states import AIHelper
from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu
from tgbot.handlers.user.consultation.utils import get_consultation
from tgbot.keyboards.inline.callback_data import StartConsultationData
from tgbot.keyboards.inline.callback_data.clear_chat_data import ClearChatData
from tgbot.keyboards.inline.callback_data.confirm_data import ConfirmData
from tgbot.keyboards.inline.confirm_keyboard import confirm_keyboard
from tgbot.states.consultation_state import Consultation

consultation_router = Router()


@consultation_router.message(Command("chat"))
@consultation_router.callback_query(StartConsultationData.filter())
async def start_consultation(message: Union[CallbackQuery, Message], state: FSMContext, dialog_manager: DialogManager):
    await state.clear()
    await dialog_manager.reset_stack(True)
    await dialog_manager.start(AIHelper.choose_role)


@consultation_router.callback_query(StateFilter(Consultation.start), ClearChatData.filter())
async def clear_chat(call: CallbackQuery,
                     repo: RequestsRepo,
                     user: User,
                     callback_data: ClearChatData):
    role_id = callback_data.role_id
    text = _("Are you sure you want to clear your chat history?")
    await call.message.edit_text(
        text,
        reply_markup=confirm_keyboard(role_id)
    )


@consultation_router.callback_query(StateFilter(Consultation.start), F.data == "exit")
async def clear_chat(call: CallbackQuery,
                     state: FSMContext,
                     dialog_manager: DialogManager):
    await call.message.delete_reply_markup()
    await state.clear()
    await dialog_manager.reset_stack()
    await dialog_manager.start(MainMenu.start)


@consultation_router.callback_query(StateFilter(Consultation.start), ConfirmData.filter())
async def clear_chat(call: CallbackQuery,
                     repo: RequestsRepo,
                     state: FSMContext,
                     callback_data: ConfirmData,
                     user: User):
    if callback_data.result:
        role_id = callback_data.role_id
        await repo.message.clear_messages(session_id=str(user.id), role_id=int(role_id))
        await call.message.edit_text(
            text=_("<b>The conversation was cleared ✅</b>")
        )
        text = _("Write your question to ⤵️")
        await call.message.answer(text=text)
        await state.set_state(Consultation.start)
    else:
        await call.message.delete()


@consultation_router.message(StateFilter(Consultation.start))
async def get_consultation_handler(message: Message,
                                   session_pool: async_sessionmaker,
                                   repo: RequestsRepo,
                                   user: User,
                                   state: FSMContext,
                                   bot: Bot):
    await get_consultation(message, session_pool, repo, user, state, bot)
