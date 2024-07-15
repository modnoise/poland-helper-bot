from sqlalchemy import Column, BIGINT, VARCHAR, Boolean, text, UUID, false, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from _domain.message_statistic import MessageStatistic
from infrastructure.database.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('uuid_generate_v4()'))
    telegram_id = Column(BIGINT, unique=True)
    username = Column(VARCHAR(128))
    full_name = Column(VARCHAR(128))
    active = Column(Boolean, server_default=false())
    messages_limit = Column(Integer)
    language = Column(VARCHAR(128), nullable=True)
    is_admin = Column(Boolean, server_default=false())
    is_verify = Column(Boolean, server_default=false())
    invite_code = Column(String(255), nullable=True)
    message_statistic: Mapped[MessageStatistic] = relationship('MessageStatistic', uselist=False)
