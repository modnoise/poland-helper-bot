from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from tgbot.dialogs.admin_dialogs.menu_dialogs.states import AdminMenu


async def go_to_main_menu(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AdminMenu.show_menu, mode=StartMode.RESET_STACK)


async def go_to_select_resources(call: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(AdminMenu.select_resource, mode=StartMode.RESET_STACK)
