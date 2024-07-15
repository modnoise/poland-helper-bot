from typing import Dict, Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from application.core.captcha import generate_captcha
from domain import User
from tgbot.commands.user_commands import set_user_defaults_commands
from tgbot.handlers.user.language.utils import send_lang_keyboard, send_captcha
from tgbot.states import SetLanguage, Captcha


class AuthorizationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data.get('user')
        state: FSMContext = data.get('state')
        bot: Bot = data.get('bot')
        if user.active and user.is_verify and user.messages_limit > 0:
            return await handler(event, data)

        if not user.is_verify:
            await set_user_defaults_commands(
                chat_id=event.from_user.id,
                bot=bot
            )
            captcha_code, captcha_image = generate_captcha()
            captcha_message = await send_captcha(bot, event.from_user.id, captcha_image)
            await state.update_data(captcha_code=captcha_code, captcha_message_id=captcha_message.message_id)
            await state.set_state(Captcha.get_result)
            return

        if not user.language:
            await send_lang_keyboard(bot, user.telegram_id)
            await state.set_state(SetLanguage.get_lang)
            return
