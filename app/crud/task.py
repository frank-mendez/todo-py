from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)

def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
    """Create a new task."""
    db_task = Task(
        **task.dict(),
        owner_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_task)
    try:
        db.commit()
        db.refresh(db_task)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating task: {str(e)}")
        raise
    return db_task

def get_task(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """Get a task by ID and owner."""
    return db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user_id
    ).first()

def get_tasks(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    completed: Optional[bool] = None
) -> List[Task]:
    """Get list of tasks with optional filters."""
    query = db.query(Task).filter(Task.owner_id == user_id)
    
    if category_id is not None:
        query = query.filter(Task.category_id == category_id)
    if completed is not None:
        query = query.filter(Task.completed == completed)
        
    return query.offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task: TaskUpdate, user_id: int) -> Optional[Task]:
    """Update task details."""
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    
    update_data = task.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    try:
        db.commit()
        db.refresh(db_task)
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating task: {str(e)}")
        raise
    return db_task

def delete_task(db: Session, task_id: int, user_id: int) -> bool:
    """Delete a task."""
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return False
    
    try:
        db.delete(db_task)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting task: {str(e)}")
        raise
    return True

def toggle_task_completion(db: Session, task_id: int, user_id: int) -> Optional[Task]:
    """Toggle task completion status."""
    db_task = get_task(db, task_id, user_id)
    if not db_task:
        return None
    
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()
    
    try:
        db.commit()
        db.refresh(db_task)
    except Exception as e:
        db.rollback()
        logger.error(f"Error toggling task completion: {str(e)}")
        raise
    return db_task
