from enum import Enum


class PaymentMethod(int, Enum):
    card = 1
    crypto = 2

    def __str__(self):
        return self.value
