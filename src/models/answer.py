import enum

from sqlalchemy import Column, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class OptionEnum(enum.Enum):
    YES = 'yes'
    NO = 'no'
    I_DONT_KNOW = 'idk'

class Answer(Base):
    __tablename__ = 'answer'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    test_taker = Column(UUID(as_uuid=True), ForeignKey('test_taker.id'), nullable=False)
    question = Column(UUID(as_uuid=True), ForeignKey('question.id'), nullable=False)
    option = Column(Enum(OptionEnum), nullable=False)
