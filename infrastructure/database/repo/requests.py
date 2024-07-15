import asyncio
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from application.core.enums import AudienceBroadcastType
from infrastructure.database.repo.admin import AdminRepo
from infrastructure.database.repo.invites import InvitesRepo
from infrastructure.database.repo.message import MessageRepo
from infrastructure.database.repo.users import UserRepo
from infrastructure.database.setup import create_engine


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def message(self) -> MessageRepo:
        return MessageRepo(self.session)

    @property
    def users(self) -> UserRepo:
        return UserRepo(self.session)

    @property
    def admin(self) -> AdminRepo:
        return AdminRepo(self.session)

    @property
    def invites(self) -> InvitesRepo:
        return InvitesRepo(self.session)


if __name__ == "__main__":
    from infrastructure.database.setup import create_session_pool
    from tgbot.config import Config, load_config


    async def example_usage(config: Config):
        """
        Example usage function for the RequestsRepo class.
        Use this function as a guide to understand how to utilize RequestsRepo for managing user data.
        Pass the config object to this function for initializing the database resources.
        :param config: The config object loaded from your configuration.
        """
        engine = create_engine(config.db)
        session_pool = create_session_pool(engine)

        async with session_pool() as session:
            repo = RequestsRepo(session)

            # Replace user details with the actual values
            result = await repo.users.get_users_for_broadcast(lang="uk",
                                                              audience=AudienceBroadcastType.HAVE_NOT_SUBSCRIPTION)
            print(result)


    config = load_config(".env")
    asyncio.run(example_usage(config))
