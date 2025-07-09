from sqlalchemy import Column, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
