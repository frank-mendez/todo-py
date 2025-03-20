from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.api.routes.auth import get_current_active_user
from app.api.routes.categories import categories_db
from app.api.errors import NotFoundError, ValidationError

router = APIRouter()

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    owner: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Temporary in-memory storage
tasks_db = {}
task_id_counter = 1

@router.post("/tasks/", response_model=Task)
async def create_task(
    task: TaskCreate,
    current_user: dict = Depends(get_current_active_user)
):
    global task_id_counter
    
    if task.category_id and task.category_id not in categories_db:
        raise NotFoundError("Category not found")

    new_task = Task(
        id=task_id_counter,
        **task.dict(),
        owner=current_user.username,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    tasks_db[task_id_counter] = new_task
    task_id_counter += 1
    return new_task

@router.get("/tasks/", response_model=List[Task])
async def get_tasks(
    current_user: dict = Depends(get_current_active_user),
    category_id: Optional[int] = None,
    completed: Optional[bool] = None
):
    tasks = [task for task in tasks_db.values() if task.owner == current_user.username]
    
    if category_id is not None:
        tasks = [task for task in tasks if task.category_id == category_id]
    if completed is not None:
        tasks = [task for task in tasks if task.completed == completed]
    
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if task_id not in tasks_db:
        raise NotFoundError("Task not found")
    task = tasks_db[task_id]
    if task.owner != current_user.username:
        raise NotFoundError("Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_update: TaskCreate,
    current_user: dict = Depends(get_current_active_user)
):
    if task_id not in tasks_db:
        raise NotFoundError("Task not found")
    task = tasks_db[task_id]
    if task.owner != current_user.username:
        raise NotFoundError("Task not found")

    if task_update.category_id and task_update.category_id not in categories_db:
        raise NotFoundError("Category not found")
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.now()
    tasks_db[task_id] = task
    return task

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if task_id not in tasks_db:
        raise NotFoundError("Task not found")
    task = tasks_db[task_id]
    if task.owner != current_user.username:
        raise NotFoundError("Task not found")
    
    del tasks_db[task_id]
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/toggle", response_model=Task)
async def toggle_task(
    task_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if task_id not in tasks_db:
        raise NotFoundError("Task not found")
    task = tasks_db[task_id]
    if task.owner != current_user.username:
        raise NotFoundError("Task not found")
    
    task.completed = not task.completed
    task.updated_at = datetime.now()
    return task
