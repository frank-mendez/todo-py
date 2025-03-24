from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped
from datetime import datetime

class Base(DeclarativeBase):
    """Base class for all models"""
    pass

class TimestampedBase(Base):
    """Base class for all models with timestamp fields"""
    __abstract__ = True

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)