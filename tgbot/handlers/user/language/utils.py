from aiogram import Bot
from aiogram.types import BufferedInputFile
from aiogram.utils.i18n import gettext as _
from six import BytesIO

from application.core.captcha import generate_captcha
from tgbot.keyboards.inline import language_keyboard


async def send_lang_keyboard(bot: Bot, telegram_id: int):
    text = _("Choose your language")
    await bot.send_message(
        chat_id=telegram_id,
        text=text,
        reply_markup=language_keyboard()
    )


async def send_captcha(bot: Bot, telegram_id: int, captcha_image: BytesIO):
    captcha_image_bytes = captcha_image.getvalue()
    captcha = BufferedInputFile(captcha_image_bytes, filename="captcha.png")
    text = _("Please enter this code for verification")
    return await bot.send_photo(chat_id=telegram_id, photo=captcha, caption=text)