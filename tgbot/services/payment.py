from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from tgbot.config import load_config
from tgbot.keyboards.inline import crypto_payment_keyboard
from tgbot.keyboards.inline.callback_data.payment_keyboard import payment_keyboard

config = load_config(".env")


async def send_crypto_payment(message: Message, payment_link: str, invoice_id: str, amount: float):
    text = _("<b>💸 After payment, click on the \"Verify Payment\" button\n\n"
             "🔰 Payment link 🔰</b>")
    await message.edit_text(
        text=text,
        reply_markup=crypto_payment_keyboard(payment_link, invoice_id, amount)
    )


async def send_card_payment_link(message: Message, payment_link: str):
    text = _("<b>🔰 Payment link 🔰</b>")
    await message.edit_text(
        text=text,
        reply_markup=payment_keyboard(payment_link)
    )
