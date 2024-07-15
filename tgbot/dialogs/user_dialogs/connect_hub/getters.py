from aiogram.enums import ContentType
from aiogram.utils.i18n import gettext as _
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from domain import User


async def menu_getter(dialog_manager: DialogManager, **middleware_data):
    user: User = middleware_data.get('user')

    match user.language:
        case 'ru':
            file_id = "CgACAgIAAxkBAAIOdmT3b2y__F-4SgH-2fGGUuQdoAsYAALsMgACkew5S3cFtzUcGF85MAQ"
        case 'uk':
            file_id = "CgACAgIAAxkBAAIQ4WUIL-r_qUqpI85eDjqz3FN78DS1AAK1NgAC7zZJSMGUnW0Llr2tMAQ"
        case _:
            file_id = "CgACAgIAAxkBAAIQ5WUIMAIuoaOk4JEl8VzD8mnE3FJhAAK2NgAC7zZJSBflySByOgwNMAQ"

    text = _("<b>Connect Hub</b>\n"
             "This is a contact book that helps you find the right professionals in Poland.")

    banner = MediaAttachment(type=ContentType.ANIMATION, file_id=MediaId(file_id))

    return {
        "text": text,
        "provide_questionnaire_button_text": _("Provide your questionnaire 📝"),
        "search_expert_button_text": _("Find an expert 🕵️‍♂️🔍"),
        "go_back": _("Back ↩️"),
        "banner": banner,
    }


async def request_for_expert_getter(dialog_manager: DialogManager, **middleware_data):
    text = _("Indicate which <b>expert</b> you are looking for 🔍\n\n"
             "And send ⤵️ information in one message")

    return {
        "text": text,
        "go_back": _("Back ↩️")
    }


async def provide_questionnaire_getter(dialog_manager: DialogManager, **middleware_data):
    text = _("Fill out the expert form 📋\n"
             "👤 <b>Name:</b> [Your name]\n\n"
             "🎓 <b>Area of expertise:</b> [Your area of expertise, e.g. manicure, fitness, marketing, etc.]\n"
             "💼 <b>Work experience:</b> [Your work experience, years, places, etc.]\n"
             "💬 <b>Briefly about yourself:</b> [A brief description of you as an expert and your approach]\n"
             "📍 <b>Location:</b> [Your location or activities]\n"
             "📞 <b>Telegram contact:</b> [Your nickname in Telegram].\n\n"
             "send ⤵️ the application form in one message")

    return {
        "text": text,
        "go_back": _("Back ↩️")
    }


async def request_confirmation_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    request = ctx.dialog_data.get("request")

    text = _("⚠️ <b>Send this request for an expert??</b>\n\n"
             "{request}").format(request=request)

    return {
        "text": text
    }


async def questionnaire_confirmation_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    questionnaire = ctx.dialog_data.get("questionnaire")

    text = _("⚠️ <b>Send this application form?</b>\n\n"
             "{questionnaire}").format(questionnaire=questionnaire)

    return {
        "text": text
    }
