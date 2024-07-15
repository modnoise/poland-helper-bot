from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button

from tgbot.dialogs.admin_dialogs.add_new_admin.states import AddNewAdmin
from tgbot.dialogs.admin_dialogs.ai_queries_dialogs.states import AIQueries
from tgbot.dialogs.admin_dialogs.broadcast.states import BroadcastMenu
from tgbot.dialogs.admin_dialogs.change_subscription.states import ChangeSubscription
from tgbot.dialogs.admin_dialogs.invites.states import Invites
from tgbot.dialogs.admin_dialogs.menu_dialogs.states import AdminMenu
from tgbot.dialogs.admin_dialogs.resources.states import Resources


async def go_to_add_admin(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AddNewAdmin.ask_username_or_telegram_id, mode=StartMode.RESET_STACK)


async def go_to_ai_queries(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AIQueries.get_user, mode=StartMode.RESET_STACK)


async def go_to_change_subscription(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(ChangeSubscription.change_subscription_menu, mode=StartMode.RESET_STACK)


async def go_to_broadcast(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(BroadcastMenu.choose_language, mode=StartMode.RESET_STACK)


async def go_to_statistics(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(AdminMenu.show_statistics)


async def on_resource_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(AdminMenu.select_resource)


async def on_invites_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(Invites.show_menu, mode=StartMode.RESET_STACK)


async def on_library_resource_click(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(Resources.library, mode=StartMode.RESET_STACK)


