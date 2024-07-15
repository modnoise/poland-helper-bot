from sqlalchemy import select, insert, func, delete, update

from domain import Invite
from infrastructure.database.repo.base import BaseRepo


class InvitesRepo(BaseRepo):
    async def get_invite(self, code: str) -> Invite:
        smt = select(
            Invite
        ).where(
            func.lower(Invite.code) == code.lower()
        )
        result = await self.session.execute(smt)
        return result.scalar()

    async def get_invite_by_id(self, invite_id: int) -> Invite:
        smt = select(
            Invite
        ).where(
            Invite.id == invite_id
        )
        result = await self.session.execute(smt)
        return result.scalar()

    async def get_invites(self) -> list[Invite]:
        smt = select(
            Invite
        ).order_by(
            Invite.created_at.desc()
        )
        result = await self.session.execute(smt)
        return result.scalars().all()

    async def add_invite(self, code: str, name: str):
        smt = insert(
            Invite
        ).values(
            code=code,
            name=name
        )
        await self.session.execute(smt)
        await self.session.commit()

    async def delete_invite_by_id(self, invite_id: int):
        sql = delete(
            Invite
        ).where(
            Invite.id == invite_id
        )
        await self.session.execute(sql)
        await self.session.commit()

    async def change_name_by_id(self, name: str, invite_id: int):
        sql = update(
            Invite
        ).values(
            name=name
        ).where(
            Invite.id == invite_id
        )
        await self.session.execute(sql)
        await self.session.commit()
