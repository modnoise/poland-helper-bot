from aiogram_dialog import DialogManager

from infrastructure.database.repo.requests import RequestsRepo


async def get_check_info(dialog_manager: DialogManager, **middleware_data):
    repo: RequestsRepo = middleware_data.get('repo')
    ctx = dialog_manager.current_context()
    admin_telegram_id = ctx.dialog_data.get('admin_telegram_id')
    admin_username = ctx.dialog_data.get('admin_username')

    text = ""
    if admin_username:
        user = await repo.users.get_user(username=admin_username)
        text = (f"<b>Підтвердження операції</b>\n\n"
                f"Username: @{admin_username}\n"
                f"Користувач: <code>{user.full_name}</code>\n\n")

    if admin_telegram_id:
        user = await repo.users.get_user(telegram_id=admin_telegram_id)
        text = (f"<b>Підтвердження операції</b>\n\n"
                f"Telegram ID: <code>{admin_telegram_id}</code>\n"
                f"Користувач: <code>{user.full_name}</code>\n\n")

    text += "Надати права адміністратора?"
    data = {
        "text": text
    }
    return data