import logging
import re
from aiogram import Router, F, Bot
from aiogram.types import Message

support_router = Router()


@support_router.message(F.reply_to_message.from_user.id == 7069311426)
async def start(message: Message, bot: Bot):
    pattern = r"#ID\d+"
    if message.reply_to_message.text:
        matches = re.findall(pattern, message.reply_to_message.text)
    else:
        matches = re.findall(pattern, message.reply_to_message.caption)

    if len(matches) > 0:
        text = message.html_text
        telegram_id = int(matches[0][3:])
        try:
            if message.audio:
                await bot.send_audio(
                    chat_id=telegram_id,
                    audio=message.audio.file_id,
                    caption=text
                )
            elif message.video_note:
                await bot.send_video_note(
                    chat_id=telegram_id,
                    video_note=message.video_note.file_id
                )
            elif message.video:
                await bot.send_video(
                    chat_id=telegram_id,
                    video=message.video.file_id,
                    caption=text
                )
            elif message.voice:
                await bot.send_voice(
                    chat_id=telegram_id,
                    voice=message.voice.file_id,
                    caption=text
                )
            elif message.document:
                await bot.send_document(
                    chat_id=telegram_id,
                    document=message.document.file_id,
                    caption=text
                )
            elif message.photo:
                await bot.send_photo(
                    chat_id=telegram_id,
                    photo=message.photo[0].file_id,
                    caption=text
                )
            elif message.text:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=text
                )
            else:
                return
        except Exception as e:
            logging.error(e)
    return
