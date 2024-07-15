from aiogram.utils.i18n import gettext as _
from aiogram_dialog import DialogManager

from domain import User
from application.core.enums import RoleEnum
from . import utils


async def choose_role_getter(dialog_manager: DialogManager, **middleware_data):
    text = _("Poland Helper 24/7 🕑 An artificial intelligence-based assistant that will help in most life situations in Poland. 🤖🇵🇱\n\n"
             "Choose the right assistant ⤵️")

    roles = [
        (_("Adaptation and relocation agent 🌍"), str(RoleEnum.AGENT_ADAPTATION_RELOCATION.value)),
        (_("Student assistant 🎓"), str(RoleEnum.STUDENT_ASSISTANT.value)),
        (_("Psychologist 🧠"), str(RoleEnum.PSYCHOLOGIST.value)),
        (_("Translator of Polish 👩‍🏫"), str(RoleEnum.POLISH_TRANSLATOR.value)),
    ]

    data = {
        "text": text,
        "roles": roles,
        "go_back": _("Back ↩️"),
        "details": _("Read More ℹ️"),
    }
    return data


async def role_details_getter(dialog_manager: DialogManager, **middleware_data):
    data = {
        "text": _("👩‍🏫 <b>Polish teacher and translator</b>\n"
                  "With his help you can easily communicate in Polish, quickly translate texts from any language into Polish and vice versa. He will help you learn Polish, correct mistakes with rule explanations and support you at every stage of language acquisition.\n\n"
                  "📘 <b>Student Assistant</b>\n"
                  "Thanks to it, you will achieve great success in your studies. He will provide you with explanations of complex topics, supplementary materials and answers to your questions so that you can deepen your understanding of the study material and achieve outstanding results.\n\n"
                  "🌍 <b>Adaptation and Relocation Agent</b>\n"
                  "For those who are moving to Poland, he is ready to be your adaptation advisor, providing information on how to deal with everyday tasks - starting with questions on finding accommodation, finding a job, using public transportation and others. He will help you with finding specific information, resources or services in Poland, simplifying the whole process and allowing you to focus on your goals and dreams.\n\n"
                  "🧠 <b>Psychologist</b>\n"
                  "The doors are always open to your thoughts and emotions. You can discuss your feelings, learn how to manage stress and find support in difficult moments. He is here to make sure you don't feel alone."),
        "go_back": _("Back ↩️")
    }
    return data


async def start_conversational_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    role_id = ctx.dialog_data.get("role_id")
    conversation_example = utils.get_conversation_example(RoleEnum(role_id))

    data = {
        "text": _("<b>Examples of questions:</b>\n"
                  "<code>{conversation_example}</code>\n\n"
                  "<b>Write your question to ⤵️</b>").format(
            conversation_example=conversation_example
        ),
        "go_back": _("Back ↩️"),
        "how_to_use": _("How to use ❔")
    }
    return data


async def how_to_use_window_getter(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    role_id = ctx.dialog_data.get("role_id")
    user: User = dialog_manager.middleware_data.get("user")

    conversation_example = utils.get_conversation_example(RoleEnum(role_id))
    tips = utils.get_tips_for_use(user.language)

    text = _("<b>Important!</b>\n"
             "To get the best results from your assistant, we recommend that you formulate your questions clearly and specifically. Avoid asking general questions.\n\n"
             "<b>For example:</b>\n"
             "\"{conversation_example}\"\n\n"
             "💡 If you change the topic of your question, we recommend clearing the chat so that the previous information you provided does not confuse the whole context\n\n"
             "To send a question, click <b>\"BACK\"</b>") \
        .format(
        conversation_example=conversation_example,
        tips=tips
    )
    return {
        "text": text,
        "go_back": _("Back ↩️")
    }
