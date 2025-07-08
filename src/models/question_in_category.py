import enum

from .base import Base

from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

class IncreaseOptionEnum(enum.Enum):
    YES_INCREASE = 'yes'
    NO_INCREASE = 'no'


class QuestionInCategory(Base):
    __tablename__ = 'question_in_category'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    category = Column(UUID(as_uuid=True), ForeignKey('category.id'), nullable=False)
    question = Column(UUID(as_uuid=True), ForeignKey('question.id'), nullable=False)
    increase_option = Column(Enum(IncreaseOptionEnum), nullable=False)
