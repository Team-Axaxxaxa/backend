from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class Category(Base):
    __tablename__ = 'category'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    name = Column(String, unique=True, nullable=False)
    is_main_category = Column(Boolean, default=False, nullable=False)
    is_shown = Column(Boolean, default=True, nullable=False)
