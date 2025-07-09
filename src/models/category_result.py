from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class CategoryResult(Base):
    __tablename__ = 'category_result'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    category = Column(UUID(as_uuid=True), ForeignKey('category.id'), nullable=False)
    result = Column(UUID(as_uuid=True), ForeignKey('result.id'), nullable=False)
    score = Column(Integer, nullable=False)
