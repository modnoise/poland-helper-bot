import json
from typing import List

from langchain.schema import messages_from_dict, _message_to_dict, BaseMessage
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.core.enums import RoleEnum
from application.services.openai.memory.chat_message_history import BaseChatMessageHistoryAsync
from domain import Message


class SQLChatMessageHistory(BaseChatMessageHistoryAsync):
    """Chat message history stored in an SQL database."""

    def __init__(
            self,
            message_history: list[Message],
            role_id: RoleEnum,
            session_id: str,
            session_pool: async_sessionmaker,
    ):
        self.message_history = message_history
        self.Message = Message
        self.role_id = role_id
        self.session_id = session_id
        self.Session = session_pool

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve all messages from db"""
        if len(self.message_history):
            items = [json.loads(record.message) for record in self.message_history]
        else:
            items = []
        messages = messages_from_dict(items)
        return messages

    async def add_message(self, message: BaseMessage) -> None:
        async with self.Session() as session:
            jsonstr = json.dumps(_message_to_dict(message), ensure_ascii=False)
            session.add(self.Message(session_id=self.session_id, message=jsonstr, role_id=self.role_id))
            await session.commit()

    async def clear(self) -> None:
        """Clear session memory from db"""
        async with self.Session() as session:
            await session.query(self.Message).filter(
                self.Message.session_id == self.session_id
            ).delete()
            await session.commit()
