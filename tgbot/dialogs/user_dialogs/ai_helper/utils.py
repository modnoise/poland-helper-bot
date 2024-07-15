from application.core.enums import RoleEnum
from aiogram.utils.i18n import gettext as _


def get_conversation_example(role: RoleEnum):
    match role:
        case RoleEnum.AGENT_ADAPTATION_RELOCATION:
            return _("Good afternoon! I am going to move to Poland. Where can I find information about rental housing and job opportunities?")
        case RoleEnum.STUDENT_ASSISTANT:
            return _("Hello! Can you explain to me the topic of differentiation in math? I am having a hard time understanding this concept.")
        case RoleEnum.PSYCHOLOGIST:
            return _("Hi, I'm worried about constant stress at work. How can I manage my emotions better?")
        case RoleEnum.POLISH_TRANSLATOR:
            return _("Hello! I'm wondering how to say 'Thank you' in Polish.")


def get_tips_for_use(language: str):
    match language:
        case "uk":
            return "https://pointed-jacket-016.notion.site/d00adefa56a146a1a995e1387ca60a5b?pvs=4"
        case "ru":
            return "https://pointed-jacket-016.notion.site/bb667e8c260f47768d37780d13dbc237?pvs=4"
        case _:
            return "https://pointed-jacket-016.notion.site/d00adefa56a146a1a995e1387ca60a5b?pvs=4"