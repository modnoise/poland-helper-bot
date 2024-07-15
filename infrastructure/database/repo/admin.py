from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import func, select

from domain import MessageStatistic, User
from infrastructure.database.repo.base import BaseRepo


@dataclass
class UserStatistics:
    active_users_24h: int
    active_users_7d: int
    new_users_24h: int
    new_users_7d: int
    total_users: int


class AdminRepo(BaseRepo):
    async def get_statistics(self) -> UserStatistics:
        now = datetime.utcnow()

        active_users_24h = await self.session.execute(
            select(func.count(MessageStatistic.user_id))
            .filter(MessageStatistic.last_message_time >= now - timedelta(days=1))
        )

        active_users_7d = await self.session.execute(
            select(func.count(MessageStatistic.user_id))
            .filter(MessageStatistic.last_message_time >= now - timedelta(days=7))
        )

        new_users_24h = await self.session.execute(
            select(func.count(User.id))
            .filter(User.created_at >= now - timedelta(days=1))
        )

        new_users_7d = await self.session.execute(
            select(func.count(User.id))
            .filter(User.created_at >= now - timedelta(days=7))
        )

        total_users = await self.session.execute(select(func.count(User.id)))

        return UserStatistics(
            active_users_24h=active_users_24h.scalar(),
            active_users_7d=active_users_7d.scalar(),
            new_users_24h=new_users_24h.scalar(),
            new_users_7d=new_users_7d.scalar(),
            total_users=total_users.scalar()
        )
