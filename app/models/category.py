from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    description = Column(String)
    
    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="categories")
    tasks = relationship("Task", back_populates="category")