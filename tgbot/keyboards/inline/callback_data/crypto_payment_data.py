from aiogram.filters.callback_data import CallbackData


class CryptoPaymentData(CallbackData, prefix="crd"):
    invoice_id: str
    amount: float