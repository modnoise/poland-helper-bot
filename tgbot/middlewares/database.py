from typing import Callable, Dict, Any, Awaitable, Optional, Union
import re
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from infrastructure.database.repo.requests import RequestsRepo


async def get_invite_code(event: Union[Message, CallbackQuery], repo: RequestsRepo) -> Optional[str]:
    if isinstance(event, CallbackQuery):
        return

    if not event.text:
        return

    pattern = r'/start (\w+)'
    match = re.search(pattern, event.text)

    if match:
        extracted_string = match.group(1)
        code = await repo.invites.get_invite(extracted_string)
        if code:
            return extracted_string


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)
            invite_code = await get_invite_code(event, repo)

            user = await repo.users.get_or_create_user(
                telegram_id=event.from_user.id,
                username=event.from_user.username,
                full_name=event.from_user.full_name,
                invite_code=invite_code
            )

            data["session_pool"] = self.session_pool
            data["repo"] = repo
            data["user"] = user

            result = await handler(event, data)
        return result
