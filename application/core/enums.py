from enum import Enum


class Language(str, Enum):
    EN = 'en',
    RU = 'ru',
    UA = "ua"


class RoleEnum(int, Enum):
    AGENT_ADAPTATION_RELOCATION = 1
    STUDENT_ASSISTANT = 2
    PSYCHOLOGIST = 3
    POLISH_TRANSLATOR = 4

    def __str__(self):
        return self.value


class SubscriptionType(int, Enum):
    DEMO = 1
    STANDARD = 2

    def __str__(self):
        return self.value


class AudienceBroadcastType(int, Enum):
    ALL = 1
    HAVE_SUBSCRIPTION = 2
    HAVE_NOT_SUBSCRIPTION = 3

    def __str__(self):
        return self.value


class LimitType(int, Enum):
    START_MASSAGES = 20

    def __str__(self):
        return self.value


class FiatCurrency(str, Enum):
    EUR = 'EUR'

    def __str__(self):
        return self.value


class InvoiceType(str, Enum):
    SUBSCRIPTION = 'subscription'
    TOKEN = 'token'

    def __str__(self):
        return self.value
