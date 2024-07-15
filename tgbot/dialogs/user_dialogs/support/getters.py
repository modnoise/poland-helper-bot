from aiogram_dialog import DialogManager
from aiogram.utils.i18n import gettext as _


async def get_message_support(dialog_manager: DialogManager, **middleware_data):
    text = _("💭 <b>Feedback is important to us!</b> We value your opinion and comments. If you have any feedback, suggestions or questions, please share them with us. Your input helps us improve our services and provide you with a better experience.\n\n"
             "Thank you for your participation! Please send your message to ⤵️")

    data = {
        "text": text,
        "go_back": _("Back ↩️"),
    }
    return data


async def get_user_question(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    question = ctx.dialog_data.get('question')

    text = _("⚠️ <b>Send this message to support?</b>\n\n"
             "{question}").format(question=question)

    data = {
        "text": text
    }
    return data
