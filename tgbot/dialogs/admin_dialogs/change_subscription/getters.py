from aiogram_dialog import DialogManager

from infrastructure.database.repo.requests import RequestsRepo


async def info_user_subscription_getter(dialog_manager: DialogManager, **middleware_data):
    repo: RequestsRepo = middleware_data.get('repo')
    ctx = dialog_manager.current_context()
    user_telegram_id = ctx.dialog_data.get('user_telegram_id')
    user = await repo.users.get_user(telegram_id=user_telegram_id)

    text = f"👤 <b>{user.full_name}</b>\n\n"

    if user.username:
        text += f"Username: @{user.username}\n\n"
    else:
        text += f"Telegram ID: <code>{user.telegram_id}</code>\n\n"

    data = {
        "text": text,
        "provide_subscription": user.subscription_detail is None,
        "cancel_subscription": user.subscription_detail is not None,
    }
    return data


async def last_check_before_edit_user_getter(dialog_manager: DialogManager, **middleware_data):
    repo: RequestsRepo = middleware_data.get('repo')
    ctx = dialog_manager.current_context()
    user_telegram_id = ctx.dialog_data.get('user_telegram_id')
    user = await repo.users.get_user(telegram_id=user_telegram_id)

    text = (f"<b>Підтвердження операції</b>\n\n"
            f"👤 {user.full_name}\n")

    if user.username:
        text += f"Username: @{user.username}\n\n"
    else:
        text += f"Telegram ID: <code>{user.telegram_id}</code>\n\n"

    if user.subscription_detail:
        text += "Скасувати підписку?"
    else:
        text += "Надати підписку?"

    data = {
        "text": text
    }
    return data
