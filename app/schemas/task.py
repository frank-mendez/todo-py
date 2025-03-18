from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskPriority(str, Enum):
    """Enum for task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    """Enum for task status"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBase(BaseModel):
    """Base schema for task"""
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None


class Task(TaskBase):
    """Schema for task response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        """Pydantic config"""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete project documentation",
                "description": "Write comprehensive documentation for API endpoints",
                "priority": "high",
                "status": "in_progress",
                "due_date": "2024-03-20T17:00:00",
                "category_id": 1,
                "user_id": 1,
                "created_at": "2024-03-18T10:00:00",
                "updated_at": "2024-03-18T11:30:00",
                "completed_at": None
            }
        }