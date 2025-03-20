from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel  # Fix the import

class Task(BaseModel):
    __tablename__ = "tasks"

    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    due_date = Column(DateTime, nullable=True)
    
    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")