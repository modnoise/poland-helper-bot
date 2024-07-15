import datetime
from typing import Optional

from sqlalchemy import select, update, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from application.core.enums import AudienceBroadcastType, LimitType
from domain import User, MessageStatistic
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):

    async def get_user_total(self):
        q = select(
            func.count(User.id)
        )
        result = await self.session.execute(q)
        return result.scalar()

    async def get_or_create_user(
            self,
            telegram_id: int,
            full_name: str,
            username: Optional[str] = None,
            invite_code: Optional[str] = None,
    ):

        insert_stmt = select(
            User
        ).options(
            selectinload(User.message_statistic),
        ).from_statement(
            insert(User)
            .values(
                telegram_id=telegram_id,
                username=username,
                full_name=full_name,
                invite_code=invite_code,
                messages_limit=0
            )
            .returning(User)
            .on_conflict_do_update(
                index_elements=[User.telegram_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                ),
            )
        )
        result = await self.session.scalars(insert_stmt)

        await self.session.commit()
        return result.first()

    async def get_users_by_lang(self, lang: str) -> list[int]:
        smt = select(
            User.telegram_id
        ).where(
            User.language == lang,
            User.active == True
        )
        result = await self.session.execute(smt)
        return result.scalars().all()

    async def get_users_for_broadcast(self, lang: str, audience: AudienceBroadcastType) -> list[int]:
        smt = select(
            User.telegram_id
        ).where(
            User.language == lang,
            User.active == True
        )

        result = await self.session.execute(smt)
        return result.scalars().all()

    async def get_user(self,
                       user_id: str = None,
                       telegram_id: int = None,
                       username: str = None) -> User:
        smt = select(User).options(
            selectinload(User.message_statistic)
        )

        if user_id:
            smt = smt.where(User.id == user_id)
        if telegram_id:
            smt = smt.where(User.telegram_id == telegram_id)
        if username:
            smt = smt.where(User.username == username)

        result = await self.session.execute(smt)
        return result.scalar()

    async def add_admin(self,
                        user_id: str = None,
                        telegram_id: int = None,
                        username: str = None):
        smt = update(User).values(is_admin=True)
        if user_id:
            smt = smt.where(User.id == user_id)
        if telegram_id:
            smt = smt.where(User.telegram_id == telegram_id)
        if username:
            smt = smt.where(User.username == username)

        await self.session.execute(smt)
        await self.session.commit()

    async def change_active(self, active: bool):
        smt = update(
            User
        ).values(
            active=active
        )
        await self.session.execute(smt)
        await self.session.commit()

    async def increase_available_queries_to_ai(self, user: User, quantity: int):
        smt = update(
            User
        ).values(
            messages_limit=user.messages_limit + quantity
        ).where(
            User.id == user.id
        )
        await self.session.execute(smt)
        await self.session.commit()

    async def set_language(self, lang: str, user_id: str):
        smt = update(
            User
        ).values(
            language=lang
        ).where(
            User.id == user_id
        )
        await self.session.execute(smt)
        await self.session.commit()

    async def track_messages_to_ai(self, user_id: str):
        user = await self.get_user(user_id)
        current_time = datetime.datetime.utcnow()
        if user.message_statistic:
            statistic = user.message_statistic
            if not statistic.last_message_time:
                user.last_message_time = datetime.datetime.utcnow()

            if statistic.last_message_time.date() == current_time.date():
                statistic.messages_today += 1

                if statistic.last_message_time.time().hour == current_time.time().hour:
                    statistic.messages_hour += 1
                else:
                    statistic.messages_hour = 1
            else:
                statistic.messages_today = 1
                statistic.messages_hour = 1
            statistic.messages_total += 1

            statistic.last_message_time = current_time
        else:
            self.session.add(MessageStatistic(
                user_id=user.id,
                messages_today=1,
                messages_hour=1,
                messages_total=1,
                last_message_time=current_time
            ))

        await self.session.commit()

    async def set_verity(self, user_id: str, result: bool):
        smt = update(
            User
        ).values(
            is_verify=result
        ).where(
            User.id == user_id
        )
        await self.session.execute(smt)
        await self.session.commit()

    async def get_count_verify_by_invite_code(self, invite_code: str):
        smt = select(
            func.count(User.id)
        ).where(
            User.invite_code == invite_code,
            User.is_verify == True
        )

        result = await self.session.execute(smt)
        return result.scalar()

    async def get_count_by_invite_code(self, invite_code: str):
        smt = select(
            func.count(User.id)
        ).where(
            User.invite_code == invite_code
        )

        result = await self.session.execute(smt)
        return result.scalar()
