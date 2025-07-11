from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class UiAnalysis(Base):
    __tablename__ = 'ui_analysis'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    result = Column(UUID(as_uuid=True), ForeignKey('result.id'), unique=True, nullable=False)
    text = Column(String, nullable=False)
