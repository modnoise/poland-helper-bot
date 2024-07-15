from datetime import datetime, timedelta
from typing import List

from sqlalchemy import select, and_, desc, delete

from infrastructure.database.repo.base import BaseRepo
from domain import Message, MessageStatistic


class MessageRepo(BaseRepo):
    async def get_messages(self, role_id: int, session_id: str) -> List[Message]:  # type: ignore
        stmt = select(
            Message
        ).where(
            and_(
                Message.session_id == session_id,
                Message.role_id == role_id
            )
        ).order_by(
            desc(Message.id)  # Спадний порядок сортування за id
        ).limit(12)
        result = await self.session.execute(stmt)
        messages = result.scalars().all()
        sorted_messages = sorted(messages, key=lambda message: message.id)
        return sorted_messages

    async def clear_messages(self, session_id: str, role_id: int):
        smt = delete(
            Message
        ).where(
            Message.session_id == session_id,
            Message.role_id == role_id
        )
        await self.session.execute(smt)
        await self.session.commit()

    async def clear_chats_inactive_users(self):
        cutoff_time = datetime.utcnow() - timedelta(minutes=15)
        stmt = (
            select(MessageStatistic)
            .join(Message, MessageStatistic.user_id == Message.session_id)
            .where(MessageStatistic.last_message_time < cutoff_time)
            .distinct(MessageStatistic.user_id)  # Add DISTINCT keyword
        )

        result = await self.session.execute(stmt)
        users = result.scalars().all()
        for user in users:
            stmt = (
                delete(Message)
                .where(Message.session_id == user.user_id)
            )
            await self.session.execute(stmt)
        await self.session.commit()
