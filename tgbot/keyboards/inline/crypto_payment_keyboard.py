from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from tgbot.keyboards.inline.callback_data.crypto_payment_data import CryptoPaymentData


def crypto_payment_keyboard(payment_link: str, invoice_id: str, amount: float):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=_("Pay"),
        url=payment_link
    )
    builder.button(
        text=_("Verify Payment 🔄"),
        callback_data=CryptoPaymentData(invoice_id=invoice_id, amount=amount)
    )
    builder.adjust(1)
    return builder.as_markup()