from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram.utils.i18n import gettext as _
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from domain import User
from infrastructure.database.repo.requests import RequestsRepo


async def main_menu_getter(dialog_manager: DialogManager, **middleware_data):
    repo: RequestsRepo = middleware_data.get('repo')
    user: User = middleware_data.get('user')

    total_users = await repo.users.get_user_total()

    message = dialog_manager.event

    statistic = user.message_statistic
    messages_total = 0
    if statistic:
        messages_total = statistic.messages_total

    text = _("<b>👤 {full_name}</b>\n\n"
             "Username: {username}\n"
             "Telegram ID: <code>{telegram_id}</code>\n\n"
             "Available queries to AI: <code>{available_queries}</code>").format(
        full_name=message.from_user.full_name,
        username="None" if not message.from_user.username else f"@{message.from_user.username}",
        telegram_id=message.from_user.id,
        available_queries=max(0, user.messages_limit - messages_total),
        total_users=total_users
    )

    match user.language:
        case 'ru':
            file_id = "CgACAgIAAxkBAAITv2UKtdBd0sd0jbvL-05qnG8KXRrXAAKvOQAC9HhRSCknJ3KLrH3LMAQ"
        case 'uk':
            file_id = "CgACAgIAAxkBAAIQxWUIGMPOv3ibpx2-xSCvJ8VBKL8ZAAJNPAAC7zZBSIU27uVucriZMAQ"
        case _:
            file_id = "CgACAgIAAxkBAAIQ22UIGybpvu2PAAGdwYQRhdQ3Bn0hfAACaDwAAu82QUjBRtbTNQ967jAE"

    banner = MediaAttachment(type=ContentType.ANIMATION, file_id=MediaId(file_id))

    data = {
        "text": text,
        "go_back": _("Back ↩️"),
        "poland_helper_button_text": _("Submit Question 💬", locale=user.language),
        "find_expert_button_text": _("Find Expert 👤", locale=user.language),
        "feedback_button_text": _("Feedback 📝", locale=user.language),
        "banner": banner
    }
    return data


async def deny_tools_access_getter(dialog_manager: DialogManager, **middleware_data):
    file_id = "AgACAgIAAxkBAAIe-2XI9eDM43kSfN2iJzXklOPO-5p7AAIT1TEbk8XoSW4Vqi8QnQtGAQADAgADcwADNAQ"
    banner = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(file_id))
    text = _(
        "This section is closed in status: DEMO\n"
        "To use the tool, you must change your status to Active.\n\n"
        "You can activate the status ✅ in your Profile 👤 ⤵️")

    return {
        "text": text,
        "go_back": _("Back ↩️"),
        "banner": banner
    }
