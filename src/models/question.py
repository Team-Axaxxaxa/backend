import enum

from sqlalchemy import Column, String, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class IncreaseOptionEnum(enum.Enum):
    YES_INCREASE = 'yes'
    NO_INCREASE = 'no'

class Question(Base):
    __tablename__ = 'question'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    category = Column(UUID(as_uuid=True), ForeignKey('category.id'), nullable=False)
    text = Column(String, nullable=False)
    for_male = Column(Boolean, nullable=False)
    increase_option = Column(Enum(IncreaseOptionEnum), nullable=False)
