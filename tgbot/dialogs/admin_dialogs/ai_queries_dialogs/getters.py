from aiogram_dialog import DialogManager

from infrastructure.database.repo.requests import RequestsRepo


async def get_limits_info(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    repo: RequestsRepo = middleware_data.get('repo')
    user_telegram_id = ctx.dialog_data.get('user_telegram_id')
    user_username = ctx.dialog_data.get('user_username')
    text = ""

    user = None
    if user_username:
        user = await repo.users.get_user(username=user_username)
        text = (f"👤 <b>{user.full_name}</b>\n"
                f"Username: @{user_username}")

    if user_telegram_id:
        user = await repo.users.get_user(telegram_id=user_telegram_id)
        text = (f"👤 <b>{user.full_name}</b>\n"
                f"Telegram ID: <code>{user_telegram_id}</code>")

    statistic = user.message_statistic
    messages_total = 0
    if statistic:
        messages_total = statistic.messages_total

    text += "\n\n<i>Натисни на кнопку щоб відредагувати.</i>"
    ctx.dialog_data.update(user_id=str(user.id))


    data = {
        "text": text,
        "available_queries": f"Лишилось запитів: {max(0, user.messages_limit - messages_total)}",
    }
    return data


async def get_text_for_input(dialog_manager: DialogManager, **middleware_data):
    text = "Введи кількість запитів, які ти хочеш додати користувачу"

    data = {
        "text": text
    }
    return data
