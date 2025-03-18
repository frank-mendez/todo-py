from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from .task import Task
from .category import Category


class UserBase(BaseModel):
    """Base schema for user"""
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str = Field(..., min_length=8, max_length=100)

    @validator('password')
    def validate_password(cls, v):
        """Validate password complexity"""
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        return v


class UserUpdate(BaseModel):
    """Schema for user updates"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class User(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool = True
    tasks: List[Task] = []
    categories: List[Category] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic config"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "tasks": [],
                "categories": [],
                "created_at": "2024-03-18T10:00:00",
                "updated_at": "2024-03-18T10:30:00"
            }
        }