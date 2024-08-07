from sqlalchemy import Column, Integer, String

from infrastructure.database.models import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
