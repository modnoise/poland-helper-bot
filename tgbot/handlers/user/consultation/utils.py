import logging

from typing import Optional

from aiogram import Bot
from aiogram.utils.i18n import gettext as _

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.services.openai.retriever import run_index_llm
from application.services.openai.roles.polish_translator.role import PolishTranslator
from application.services.openai.roles.psychologist.role import Psychologist
from application.services.openai.roles.student_assistant.role import StudentAssistant
from domain import User
from application.core.enums import RoleEnum, LimitType
from application.services.openai.chain import run_llm, LLMArgs
from application.services.openai.roles.agent_adaptation import AgentAdaptationRelocation
from infrastructure.database.repo.errors import MessageLimitExceeded
from infrastructure.database.repo.requests import RequestsRepo
from tgbot.handlers.user.consultation.llm_result import LLMResults
from tgbot.keyboards.inline import update_tariff_plan_keyboard
from tgbot.keyboards.inline.callback_data.consultation_keyboard import consultation_keyboard


def format_lang(user_language: str) -> str:
    if user_language == "uk":
        return "Ukrainian"
    elif user_language == "ru":
        return "Russian"
    else:
        return "English"


def load_ai_role(role: RoleEnum, user: User):
    match role:
        case RoleEnum.AGENT_ADAPTATION_RELOCATION:
            return AgentAdaptationRelocation.load_role(user.language)
        case RoleEnum.STUDENT_ASSISTANT:
            return StudentAssistant.load_role(user.language)
        case RoleEnum.PSYCHOLOGIST:
            return Psychologist.load_role(user.language)
        case RoleEnum.POLISH_TRANSLATOR:
            return PolishTranslator.load_role(user.language)


def calculate_message_limits(user: User):
    if user.message_statistic:
        statistic = user.message_statistic
        messages_total = statistic.messages_total
        messages_limit = user.messages_limit

        if messages_total >= messages_limit:
            raise MessageLimitExceeded()


async def handle_message_limit(user: User):
    text = _(
        "<b>⚠️ You have exceeded the message limit.</b>\n"
        "<i>For more details, you can check your profile.</i>"
    ).format(limit=user.messages_limit)
    markup = None

    if not user.subscription_detail and user.message_statistic.messages_total >= LimitType.START_MASSAGES:
        text = _(
            "We're glad you're using our Demo subscription! Your current plan allows you to send up to <b>20</b> messages.\n\n"
            "If you'd like to increase your messaging limit and access more features, you can easily upgrade your plan. Just tap the button below to start the upgrade process.")

        markup = update_tariff_plan_keyboard()


    return text, markup


async def check_message_limit(user: User, bot: Bot) -> bool:
    telegram_id = user.telegram_id
    try:
        calculate_message_limits(user)
    except MessageLimitExceeded:
        text, markup = await handle_message_limit(user)

        await bot.send_message(
            chat_id=telegram_id,
            text=text,
            reply_markup=markup
        )
        return False

    return True


async def handle_error_response(message_with_response: Message):
    text = _("Oops. Something went wrong, try again later.")
    await message_with_response.edit_text(text=text)


async def get_llm_response(user: User, session_pool: async_sessionmaker, repo: RequestsRepo, question: str,
                           state: FSMContext) -> Optional[LLMResults]:
    data = await state.get_data()
    role = data.get("role")
    messages = await repo.message.get_messages(role_id=role, session_id=str(user.id))
    ai_role = load_ai_role(role, user)

    llm_args = LLMArgs(
        messages=messages,
        session_id=str(user.id),
        question=question,
        session_pool=session_pool,
        ai_role=ai_role,
        language=format_lang(user.language)
    )
    try:
        if ai_role.index_name:
            result = await run_index_llm(llm_args)
        else:
            result = await run_llm(llm_args)

        return LLMResults(text=result, ai_role=ai_role)
    except Exception as e:
        logging.error(e)


async def get_consultation(message: Message,
                           session_pool: async_sessionmaker,
                           repo: RequestsRepo,
                           user: User,
                           state: FSMContext,
                           bot: Bot):
    result_check = await check_message_limit(user, bot)

    if result_check:
        message_with_response = await message.answer(text=_("Loading..."))

        question = message.text

        if not question:
            await handle_error_response(message_with_response)
            return

        llm_result = await get_llm_response(user, session_pool, repo, question, state)

        if not llm_result or not llm_result.text:
            await handle_error_response(message_with_response)
            return

        await message_with_response.edit_text(
            llm_result.text,
            reply_markup=consultation_keyboard(role_id=llm_result.ai_role.role_id.value), disable_web_page_preview=True)
        await repo.users.track_messages_to_ai(user.id)
