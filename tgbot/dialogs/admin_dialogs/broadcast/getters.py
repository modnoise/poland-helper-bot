from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from application.core.enums import AudienceBroadcastType


async def get_text_to_ask_message(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    edit_mode = ctx.dialog_data.get('edit_mode')

    text = (f"<b>Надішліть повідомленя для розсилки.</b>\n"
            f"<i>Може бути будь-що — текст, фото, відео чи файл.</i>")
    if edit_mode:
        text = (f"<b>Будь ласка, надішліть те, що ви б хотіли додати або змінити.</b>\n"
                f"<i>Це може бути текст, фотографія, відео або файл.</i>")

    if edit_mode is None:
        edit_mode = False

    data = {
        "text": text,
        "go_to_select_lang": not edit_mode,
        "go_to_edit_menu": edit_mode
    }

    return data


async def get_langs_to_choose(dialog_manager: DialogManager, **middleware_data):
    data = {
        "langs": [("EN", "en"), ("UA", "uk"), ("RU", "ru")]
    }
    return data


async def choose_audience_type_getter(dialog_manager: DialogManager, **middleware_data):
    data = {
        "audiences": [
            ("Усі", str(AudienceBroadcastType.ALL.value)),
            ("Мають підписку", str(AudienceBroadcastType.HAVE_SUBSCRIPTION.value)),
            ("Не мають підписку", str(AudienceBroadcastType.HAVE_NOT_SUBSCRIPTION.value))
        ]
    }
    return data


async def get_message(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    photo_id = ctx.dialog_data.get('photo_id')
    video_id = ctx.dialog_data.get('video_id')
    document_id = ctx.dialog_data.get('document_id')
    text = ctx.dialog_data.get('text')

    media = None
    if photo_id:
        media = MediaAttachment(ContentType.PHOTO, url=photo_id)

    if video_id:
        media = MediaAttachment(ContentType.VIDEO, url=video_id)

    if document_id:
        media = MediaAttachment(ContentType.DOCUMENT, url=document_id)

    data = {
        "media": media if media else None,
        "text": text if text else None
    }

    return data


async def get_last_check_text(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    lang_code = ctx.dialog_data.get('lang')
    audience_id = ctx.dialog_data.get('audience_id')
    audience_type = AudienceBroadcastType(audience_id)

    audience_text = ""
    if audience_type == AudienceBroadcastType.HAVE_NOT_SUBSCRIPTION:
        audience_text = " <u>та не має підписки</u>"
    if audience_type == AudienceBroadcastType.HAVE_SUBSCRIPTION:
        audience_text = " <u>та має підписку</u>"

    language = None
    if lang_code == 'en':
        language = "англійською"
    if lang_code == 'uk':
        language = "українською"
    if lang_code == 'ru':
        language = "російською"

    data = {
        "text": (f"Відправити це повідомлення до аудиторії, яка спілкується <b>{language}</b> мовою{audience_text}?")
    }
    return data

