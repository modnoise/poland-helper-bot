from aiogram import Dispatcher
from aiogram_dialog import setup_dialogs

from tgbot.dialogs.admin_dialogs import (menu_dialogs, add_new_admin, broadcast, resources,
                                         invites, change_subscription, ai_queries_dialogs)
from tgbot.dialogs.user_dialogs import support, main_menu, ai_helper, connect_hub


def setup_all_dialogs(dp: Dispatcher):
    for dialog in [
        *menu_dialogs.menu_dialogs(),
        *add_new_admin.add_new_admin_dialogs(),
        *ai_queries_dialogs.ai_queries_dialogs(),
        *change_subscription.change_subscription_dialogs(),
        *broadcast.broadcast_dialogs(),   
        *resources.resources_dialogs(),
        *invites.invites_dialogs(),
        *main_menu.main_menu_dialogs(),
        *ai_helper.ai_helper_dialogs(),
        *support.support_dialogs(),
        *connect_hub.connect_hub_dialogs()
    ]:
        dp.include_router(dialog)
    setup_dialogs(dp)
