from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Question(Base):
    __tablename__ = 'question'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    text = Column(String, nullable=False)
    for_male = Column(Boolean, nullable=False)
