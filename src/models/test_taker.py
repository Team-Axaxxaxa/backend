from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class TestTaker(Base):
    __tablename__ = 'test_taker'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    result = Column(UUID(as_uuid=True), ForeignKey('result.id'), nullable=True)
    is_male = Column(Boolean)
