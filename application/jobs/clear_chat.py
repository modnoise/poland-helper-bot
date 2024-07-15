from application.core.scheduler import SchedulerData
from infrastructure.database.repo.requests import RequestsRepo


async def clear_chat(data: SchedulerData):
    async with data.session_pool() as session:
        repo = RequestsRepo(session)
        await repo.message.clear_chats_inactive_users()