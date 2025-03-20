from sqlalchemy import Column, Integer
from app.models.base import Base

# Import all models for Alembic
from app.models.user import User  # noqa
from app.models.task import Task  # noqa
from app.models.category import Category  # noqa

__all__ = ["Base", "User", "Category", "Task"]
