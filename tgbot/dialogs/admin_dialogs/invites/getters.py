from aiogram_dialog import DialogManager

from infrastructure.database.repo.requests import RequestsRepo


async def invites_list_getter(dialog_manager: DialogManager, **middleware_data):
    repo: RequestsRepo = middleware_data.get('repo')
    invites = await repo.invites.get_invites()

    invites_data = [(invite.name if invite.name else invite.code, invite.id) for invite in invites]

    data = {
        "invites_data": invites_data
    }

    return data


async def invite_editor_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    repo: RequestsRepo = middleware_data.get('repo')
    invite_id = ctx.dialog_data.get('invite_id')
    invite = await repo.invites.get_invite_by_id(invite_id)
    created_date = invite.created_at.strftime('%d.%m.%Y')

    bot_data = await dialog_manager.event.bot.me()
    invite_name = invite.name if invite.name else invite.code


    link = f"https://t.me/{bot_data.username}?start={invite.code}"
    text = (f"🔗 Інвайт <b>{invite_name}</b>\n"
            f"Дата створення: <code>{created_date}</code>\n\n"
            f"<code>{link}</code>")
    return {
        "text": text
    }


async def confirm_delete_invite_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    repo: RequestsRepo = middleware_data.get('repo')
    invite_id = ctx.dialog_data.get('invite_id')
    invite = await repo.invites.get_invite_by_id(invite_id)
    created_date = invite.created_at.strftime('%d.%m.%Y')

    bot_data = await dialog_manager.event.bot.me()

    invite_name = invite.name if invite.name else invite.code

    link = f"https://t.me/{bot_data.username}?start={invite.code}"
    text = (f"<b>Видалити наступний інвайт?</b>\n\n"
            f"🔗 Інвайт <b>{invite_name}</b>\n"
            f"Дата створення: <code>{created_date}</code>\n\n"
            f"<code>{link}</code>")
    return {
        "text": text
    }


async def get_analytics_by_invite_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    invite_code = ctx.dialog_data.get('invite_code')
    repo: RequestsRepo = middleware_data.get('repo')

    if not invite_code:
        invite_id = ctx.dialog_data.get('invite_id')
        invite = await repo.invites.get_invite_by_id(invite_id)
        invite_code = invite.code
    else:
        invite = await repo.invites.get_invite(invite_code)

    bot_data = await dialog_manager.event.bot.me()

    invite_name = invite.name if invite.name else invite.code
    total_users = await repo.users.get_count_by_invite_code(invite_code)
    total_verify_users = await repo.users.get_count_verify_by_invite_code(invite_code)
    link = f"https://t.me/{bot_data.username}?start={invite_code}"

    return {
        "text": (f"🔗 Інвайт: <b>{invite_name}</b>\n"
                 f"<code>{link}</code>\n\n"
                 f"Усього перейшли: <code>{total_users}</code>\n\n"
                 f"Пройшли капчу: <code>{total_verify_users}</code>\n\n")
    }
