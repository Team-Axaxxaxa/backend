from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

class AffiliateLink(Base):
    __tablename__ = 'affiliate_link'

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, server_default=func.gen_random_uuid())
    test_taker = Column(UUID(as_uuid=True), ForeignKey('test_taker.id'), nullable=True)
    author = Column(UUID(as_uuid=True), ForeignKey('admin.id'), nullable=False)
    note = Column(String, nullable=True)
