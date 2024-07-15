from sqlalchemy import Column, Integer, Text, ForeignKey, UUID, Enum
from infrastructure.database.models import Base


class Message(Base):
    __tablename__ = "message_store"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text)
