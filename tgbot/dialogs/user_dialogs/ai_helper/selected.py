from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Button
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain import User
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.dialogs.user_dialogs.ai_helper.states import AIHelper
from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu
from tgbot.handlers.user.consultation.utils import get_consultation
from tgbot.states.consultation_state import Consultation


async def goto_main_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(MainMenu.start, mode=StartMode.RESET_STACK)


async def goto_how_to_use(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(AIHelper.how_to_use)


async def goto_start_conversational(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(AIHelper.start_conversational)


async def goto_choose_role(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(AIHelper.choose_role)


async def on_role_details(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(AIHelper.role_details)


async def on_select_role(call: CallbackQuery, widget: Select, manager: DialogManager, item_id: str):
    if item_id == "soon":
        return

    ctx = manager.current_context()
    ctx.dialog_data.update(role_id=int(item_id))
    await manager.switch_to(AIHelper.start_conversational)


async def on_entered_question(message: Message, widget: TextInput, manager: DialogManager, question: str):
    ctx = manager.current_context()
    user: User = manager.middleware_data.get("user")
    repo: RequestsRepo = manager.middleware_data.get("repo")
    session_pool: async_sessionmaker = manager.middleware_data.get("session_pool")
    state: FSMContext = manager.middleware_data.get("state")
    role_id = ctx.dialog_data.get("role_id")
    await manager.done()

    await state.set_state(Consultation.start)
    await state.update_data(role=role_id)
    await get_consultation(message, session_pool, repo, user, state, bot=message.bot)
