from datetime import datetime
from typing import Any
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql import func

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class TimestampMixin:
    """Timestamp mixin for models."""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class BaseModel(Base, TimestampMixin):
    """Base model class that includes common fields."""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"

    def dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BaseModel":
        """Create model instance from dictionary."""
        return cls(**data)
