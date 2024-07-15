from sqlalchemy import text, Column, UUID, Integer, TIMESTAMP, ForeignKey

from infrastructure.database.models import Base


class MessageStatistic(Base):
    __tablename__ = 'message_statistics'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    messages_total = Column(Integer, default=0)
    messages_today = Column(Integer, default=0)
    messages_hour = Column(Integer, default=0)
    last_message_time = Column(TIMESTAMP)

