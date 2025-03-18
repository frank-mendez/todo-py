from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    """Base schema for category"""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#000000", pattern="^#[0-9a-fA-F]{6}$")
    description: Optional[str] = Field(None, max_length=200)


class CategoryCreate(CategoryBase):
    """Schema for creating a category"""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9a-fA-F]{6}$")
    description: Optional[str] = Field(None, max_length=200)


class Category(CategoryBase):
    """Schema for category response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Work",
                "color": "#FF5733",
                "description": "Work-related tasks",
                "user_id": 1,
                "created_at": "2024-03-18T10:00:00",
                "updated_at": "2024-03-18T10:30:00"
            }
        }