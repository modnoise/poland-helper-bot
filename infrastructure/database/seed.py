from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from domain import Role


async def seed_data(session_pool: async_sessionmaker):
    async with session_pool() as session:
        result = await session.execute(select(Role))
        roles_data_exists = result.first()
        if not roles_data_exists:
            roles = [Role(id=1, name="Агент з адаптації та переїзду"),
                     Role(id=2, name="Помічник студента"),
                     Role(id=3, name="Психолог"),
                     Role(id=4, name="Перекладач")]
            session.add_all(roles)

        await session.commit()
