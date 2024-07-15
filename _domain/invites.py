from sqlalchemy import Column, Integer, String

from infrastructure.database.models import Base
from infrastructure.database.models.base import TimestampMixin


class Invite(Base, TimestampMixin):
    __tablename__ = 'invites'
    id = Column(Integer, primary_key=True)
    code = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=True)
