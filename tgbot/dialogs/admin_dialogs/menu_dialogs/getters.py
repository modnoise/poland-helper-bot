from aiogram_dialog import DialogManager

from infrastructure.database.repo.requests import RequestsRepo


async def get_main_menu(dialog_manager: DialogManager, **middleware_data):
    data = {
        "text": (f"Вітаю <b>{dialog_manager.event.from_user.full_name}</b>!\n\n"
                 f"<i>Обери що тебе цікавить.</i>")
    }
    return data


async def get_statistics(dialog_manager: DialogManager, **middleware_data):
    repo: RequestsRepo = middleware_data.get('repo')
    stats = await repo.admin.get_statistics()

    data = {
        "text": (f"<b>Користувачі 👥</b>\n\n"
                 f"- Активні\n"
                 f"За 24г: <code>{stats.active_users_24h}</code>\n"
                 f"За 7 днів: <code>{stats.active_users_7d}</code>\n\n"
                 f"- Нові\n"
                 f"За 24г: <code>{stats.new_users_24h}</code>\n"
                 f"За 7 днів: <code>{stats.new_users_7d}</code>\n\n")
    }

    return data


