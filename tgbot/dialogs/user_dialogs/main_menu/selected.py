from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button

from tgbot.dialogs.user_dialogs.ai_helper.states import AIHelper
from tgbot.dialogs.user_dialogs.connect_hub.states import ConnectHub
from tgbot.dialogs.user_dialogs.main_menu.states import MainMenu
from tgbot.dialogs.user_dialogs.support.states import Support


async def on_info_center_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(MainMenu.info_center_menu)


async def on_profile_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(MainMenu.profile)


async def on_feedback_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(Support.get_question)


async def on_helper_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AIHelper.choose_role, mode=StartMode.RESET_STACK)


async def on_hub_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(ConnectHub.menu, mode=StartMode.RESET_STACK)

async def on_entered_request(message: Message, widget: TextInput, manager: DialogManager, request: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(request=request)
    await manager.switch_to(MainMenu.confirmation_request)


async def goto_main_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(MainMenu.start, mode=StartMode.RESET_STACK)

